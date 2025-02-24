from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services.qa_service import MedicalQAService
from app.models.schema import QAResponse

app = FastAPI(title="Medical QA System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize QA system
print("Initializing Medical QA System...")
qa_service = MedicalQAService(base_path='/Users/mubashirshariq/Q-A_PDF_CHAT/backend/data/medical_documents')
print("System initialization complete!")

@app.post("/ask_question/", response_model=QAResponse)
async def ask_question(question: str):
    try:
        return await qa_service.get_answer(question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat_history/")
async def get_chat_history():
    return {"chat_history": qa_service.chat_history}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)