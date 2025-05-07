from fastapi import APIRouter, File, UploadFile, HTTPException

from typing import Optional
from backend.utils.parser import extract_text_from_file
from backend.utils.vector_store import embed_and_store

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try: 
        content = await file.read()
        text = extract_text_from_file(file.filename, content)

        #embed and store
        embed_and_store(text, doc_id=file.filename)
        
        return {"filename": file.filename, "extracted_text": text[:3000]}

        
    except Exception as e:
        raise  HTTPException(status_code=400, detail=str(e))
