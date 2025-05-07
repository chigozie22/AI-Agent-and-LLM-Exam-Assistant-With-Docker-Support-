from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import upload, search, generate
from backend.routers import summarize
from backend.agent.graph_with_memory import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api")
app.include_router(search.router,prefix="/api")
app.include_router(generate.router, prefix="/api")
app.include_router(summarize.router, prefix="/api")


@app.get("/")
def read_root():
    return{"message": "Learning Agent"}



# 👇 Route to send a POST to /agent/invoke
@app.post("/invoke-agent")
async def invoke_agent(
    lecture_file: UploadFile = File(...),
    query: str = Form(...),
    past_questions: str = Form("")
):
    content = await lecture_file.read()
    result = run_agent(
        lecture_file=content,
        lecture_filename = lecture_file.filename,
        query = query,
        past_questions=past_questions
    )
    return {"response": result}
    
