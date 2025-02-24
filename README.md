# Medical Q&A

This repository contains a web application for Medical Q&A . The frontend is built with React, and the backend is powered by FastAPI. 


## Tech Stack

- **Frontend**: React
- **Backend**: FastAPI
- **LLM**: llama3(Ollama)

## Setup Instructions

### Prerequisites

- [Python 3.10+](https://www.python.org/)
- [venv](https://docs.python.org/3/library/venv.html) (for creating virtual environments)

### Frontend Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/Mubashirshariq/Q-A_PDF_CHAT.git](https://github.com/Mubashirshariq/MEDIC_CHAT.git
    ```

2. Navigate to the `frontend` directory:
    ```sh
    cd frontend
    ```

3. Install the dependencies:
    ```sh
    npm install
    ```

4. Start the frontend development server:
    ```sh
    npm run dev
    ```

### Backend Setup
Now create one more terminal to run the backend
1. Navigate to the `backend` directory:
    ```sh
    cd backend
    ```

2. Create a virtual environment:
    ```sh
    python -m venv myenv
    ```

4. Activate the virtual environment:
    - On Windows:
        ```sh
        myenv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source myenv/bin/activate
        ```

5. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

6. Run the FastAPI server:
    ```sh
     python -m app.main
    ```

 ## documentation
## **1. Data Ingestion**
###  Purpose:
Load and process medical documents (clinical guidelines, patient education materials).

###  Steps:
1. Reads `.txt` files from predefined directories (`clinical_guidelines`, `patient_education`).
2. Splits the text into **manageable chunks** using `CharacterTextSplitter`.
3. Extracts metadata (title, source, file path) for reference.
4. Converts the chunks into **embeddings** using `HuggingFaceEmbeddings`.
5. Stores them in a **FAISS vector database** for efficient retrieval.

###  Key Code:
```python
self.vectorstore = FAISS.from_texts(
    texts=texts,
    embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
    metadatas=metadatas
)   
```

## 2.  Retrieval System
### Purpose:
Retrieve the most relevant medical information based on user queries.

### Steps:
1. Uses FAISS to fetch the top K (default = 5) most relevant text chunks.
2. Retrieves metadata (title, author, link) for citations.
3. Sends retrieved context to Ollama LLM for answer generation.
### Key Code:
```python
retriever = self.vectorstore.as_retriever(search_kwargs={"k": self.TOP_K_RESULTS})
```

## 3. LLM Integration
### Purpose:
Generate human-like responses based on retrieved medical data.

### Steps:
1. Uses Ollama (llama3 model) for text generation.
2. Processes user questions and contextual information.
3. Ensures the answer follows predefined guidelines:
4. Uses only the provided context.
5. If uncertain, acknowledges limitations.
6. Provides relevant citations.

###  Key Code:
```python
llm = Ollama(model="llama3")
response = self.conversation_chain({'query': question})
```

## 4. References & Citations
## Purpose:
Provide sources for medical responses to ensure credibility.

###  Steps:
1. Extracts metadata from retrieved documents.
2. Formats citations with:
Title
Author
Link (if available)
Page number (if applicable)
Content snippet
3. Displays citations in the API response.
###  Key Code:
``` python
citations = [
    Source(
        title=source.metadata.get("title", "Unknown"),
        author=source.metadata.get("author", "Unknown"),
        link=source.metadata.get("link", None),
        page=source.metadata.get("page", None),
        content=source.page_content
    ) for source in sources
]
```

## 5. Disclaimers & Confidence Level
## Purpose:
Ensure users understand the system's limitations.

###  Steps:
1. Includes a medical disclaimer in every response.
2. Assesses confidence level based on:
No sources found → Low confidence
1-2 sources → Medium confidence
3+ sources → High confidence
###  Key Code:
``` python
def assess_confidence(self, sources: List[Source]) -> str:
    if not sources:
        return "Low - No sources found"
    elif len(sources) >= 3:
        return "High - Multiple consistent sources"
    else:
        return "Medium - Limited sources"
```
## Usage

### Example Response
<img width="1457" alt="Screenshot 2025-02-24 at 2 50 56 PM" src="https://github.com/user-attachments/assets/2eb2642a-dce6-4010-8520-b9a32d6259ca" />

### Example Citations
<img width="1446" alt="Screenshot 2025-02-24 at 2 51 09 PM" src="https://github.com/user-attachments/assets/c7d1879b-0221-4228-8193-107dc636185a" />

###Example FollowUps
<img width="1446" alt="Screenshot 2025-02-24 at 3 02 57 PM" src="https://github.com/user-attachments/assets/c1cab823-29ed-434f-ba95-a15b9fc0fe7e" />

Once both the frontend and backend servers are running, you can access the application by navigating to `http://localhost:5173` in your web browser.
