from typing import List, Optional
from pydantic import BaseModel

class Source(BaseModel):
    title: str
    author: Optional[str]
    link: Optional[str]
    page: Optional[int]
    content: str

class QAResponse(BaseModel):
    answer: str
    citations: List[Source]
    follow_up_questions: List[str]
    disclaimer: str
    confidence_level: str