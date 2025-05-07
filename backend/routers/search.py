from fastapi import APIRouter, Query
from backend.utils.vector_store import search_similar_chunks
from backend.utils.llm_engine import ask_llm 
from pydantic import BaseModel
# import numpy as np


router = APIRouter()

@router.get("/search/")
def search_documents(q: str = Query(..., description=" Search query")):
    try: 
        results = search_similar_chunks(q, top_k=5)
        return {"query": q, "results": results}
    except Exception as e:
        return {"error": str(e)}

class QueryRequest(BaseModel):
    query: str
    
@router.post("/ask/")
def ask(payload:QueryRequest):
    query = payload.query
    chunks = search_similar_chunks(query)
    if not chunks:
        return {"answer": "No relevant documents ask"}
    
    context = "\n\n".join([c["text"] for c in chunks])
    answer = ask_llm(query, context)
    return {"answer": answer,
            "chunks_used": chunks}