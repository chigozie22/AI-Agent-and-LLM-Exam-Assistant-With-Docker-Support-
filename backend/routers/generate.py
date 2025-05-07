from fastapi import APIRouter, Form, File, UploadFile, HTTPException
import os 
from fastapi.responses import JSONResponse
from backend.utils.generator import generate_possible_questions
from backend.utils.generator_parser import extract_text, extract_questions


router = APIRouter()

DATA_DIR = "/data/combined_uploads"
# os.makedirs(DATA_DIR, exist_ok=True)

@router.post("/generate-questions-without-agent/")
async def generate_questions_without_agent(
    notes: UploadFile = File(...),
    past_questions: UploadFile = File(...),
    num_questions: int = Form(...)
):
    
    try:
        notes_content = await notes.read()
        past_content = await past_questions.read()

        note_text = extract_text(notes.filename, notes_content)
        past_text = extract_questions(past_questions.filename, past_content)


        generated_questions = generate_possible_questions(note_text, past_text, num_questions)

        return {
            "status": "success",
            "generated_questions": generated_questions,
            "lecture_notes_preview": note_text[:300],
            "past_qsts_preview": past_text[:300]
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
