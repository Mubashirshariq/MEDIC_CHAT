from typing import List, Dict, Any
from langchain.text_splitter import CharacterTextSplitter

class TextProcessor:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len
        )
        return text_splitter.split_text(text)

    @staticmethod
    def extract_metadata(file_path: str) -> Dict[str, Any]:
        """Extract metadata from file path"""
        import os
        filename = os.path.basename(file_path)
        folder = os.path.basename(os.path.dirname(file_path))
        
        return {
            "title": filename,
            "source_type": folder,
            "file_path": file_path,
        }