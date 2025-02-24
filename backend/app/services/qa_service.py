import os
from typing import List, Dict, Any
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage

from app.models.schema import QAResponse, Source
from app.utils.text_processing import TextProcessor
from app.services.conversation_service import ConversationService
from app.core.constants import MEDICAL_DISCLAIMER

class MedicalQAService:
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.vectorstore = None
        self.conversation_chain = None
        self.chat_history = []
        self.TOP_K_RESULTS = 5
        self.text_processor = TextProcessor()
        
        # Initialize system
        self.process_documents()
        self.setup_qa_chain()

    def read_document(self, file_path: str) -> Dict[str, Any]:
        """Read and extract text from a document file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        metadata = self.text_processor.extract_metadata(file_path)
        return {
            "content": content,
            "metadata": metadata
        }

    def process_documents(self):
        """Process all documents from the specified folders"""
        print("Starting document processing...")
        texts = []
        metadatas = []
        
        for folder in ['clinical_guidelines', 'patient_education']:
            folder_path = os.path.join(self.base_path, folder)
            if not os.path.exists(folder_path):
                print(f"Warning: Folder {folder_path} does not exist")
                continue
                
            print(f"Processing folder: {folder}")
            for filename in os.listdir(folder_path):
                if filename.endswith('.txt'):
                    file_path = os.path.join(folder_path, filename)
                    try:
                        print(f"Processing file: {filename}")
                        doc_data = self.read_document(file_path)
                        chunks = self.text_processor.chunk_text(doc_data['content'])
                        
                        texts.extend(chunks)
                        chunk_metadata = [{
                            **doc_data['metadata'],
                            'chunk_index': i
                        } for i in range(len(chunks))]
                        metadatas.extend(chunk_metadata)
                        
                    except Exception as e:
                        print(f"Error processing file {filename}: {str(e)}")
                        continue

        print("Creating vector store...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        self.vectorstore = FAISS.from_texts(
            texts=texts,
            embedding=embeddings,
            metadatas=metadatas
        )
        print("Document processing complete!")

    def setup_qa_chain(self):
        """Initialize the QA chain with the processed vectorstore"""
        llm = Ollama(model="llama3")
        
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
            You are a medical information assistant. Use only the provided context and generally accepted medical knowledge to answer the question.
            
            Context: {context}
            Question: {question}

            Requirements:
            1. Only use information from the provided context
            2. If uncertain or if context is insufficient, acknowledge limitations
            3. Provide clear, factual information
            4. Include relevant source citations

            Answer:
            """
        )
        
        self.conversation_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": self.TOP_K_RESULTS}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )

    def generate_follow_up_questions(self, context: str, current_question: str) -> List[str]:
        prompt = f"""
        Based on the following context and previous question, generate 2-3 relevant follow-up questions:
        Context: {context}
        Previous Question: {current_question}
        Generate questions that would help deepen understanding of the topic.
        """
        llm = Ollama(model="llama3")
        response = llm.invoke(prompt)
        questions = [q.strip() for q in response.split('\n') if '?' in q][:3]
        return questions

    def assess_confidence(self, sources: List[Source]) -> str:
        if not sources:
            return "Low - No sources found"
        elif len(sources) >= 3:
            return "High - Multiple consistent sources"
        else:
            return "Medium - Limited sources"

    async def get_answer(self, question: str) -> QAResponse:
        # Check for conversation patterns first
        conv_type = ConversationService.detect_conversation_type(question)
        if conv_type:
            return ConversationService.get_conversation_response(conv_type)

        # If not a conversation, proceed with medical QA
        if not self.conversation_chain:
            raise Exception("QA system not properly initialized")

        response = self.conversation_chain({'query': question})
        answer = response.get('result', 'Insufficient information to answer the question.')
        sources = response.get('source_documents', [])

        citations = [
            Source(
                title=source.metadata.get("title", "Unknown"),
                author=source.metadata.get("author", "Unknown"),
                link=source.metadata.get("link", None),
                page=source.metadata.get("page", None),
                content=source.page_content
            ) for source in sources
        ]

        follow_ups = self.generate_follow_up_questions(
            context="\n".join([s.content for s in citations]),
            current_question=question
        )

        confidence = self.assess_confidence(citations)

        qa_response = QAResponse(
            answer=answer,
            citations=citations,
            follow_up_questions=follow_ups,
            disclaimer=MEDICAL_DISCLAIMER,
            confidence_level=confidence
        )

        self.chat_history.extend([
            HumanMessage(content=question),
            HumanMessage(content=str(qa_response))
        ])

        return qa_response