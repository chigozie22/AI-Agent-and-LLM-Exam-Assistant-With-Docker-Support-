from sentence_transformers import SentenceTransformer, util
from backend.utils.parser import extract_text_from_file
from fastapi import APIRouter, Query, File, Form,UploadFile
from llama_cpp import Llama 


router = APIRouter()


model = SentenceTransformer("all-MiniLM-L6-v2")
llm = Llama(model_path="models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf", n_ctx=2048)


def refine_summary_with_llm(extracted_summary: str, query:str)->str:
    prompt = f"""
    You are a precise assistant helping a student prepare for exams.
    Use ONLY the content in the provided notes below to respond to the student's question.
    DO NOT add your own knowledge. If the notes do not answer the question, say "Not found in the notes."

    --- CONTENT START ---
    {extracted_summary}
    ---- CONTENT END ---

    User Query: {query}

    Give a concise and clear summary.

"""
    output = llm(prompt, max_tokens=512, stop=["</s>"])
    return output["choices"][0]["text"].strip()

@router.post("/summarize/")
async def summarize_text(
    notes: UploadFile = File(...),
    query: str = Form(...)

    ) -> dict:
    try:
        file_bytes = await notes.read()
        filename = notes.filename 

        text = extract_text_from_file(filename, file_bytes)
        sentences = [s.strip() for s in text.split('.') if s.strip()]

        if not sentences:
            return {"summary": "No valid sentences found for summarization."}

        embeddings = model.encode(sentences, convert_to_tensor=True)
        query_embedding = model.encode([query], convert_to_tensor=True)
        #compute similarity 

        cosine_scores = util.cos_sim(query_embedding, embeddings)[0]

        #rank byrelevance 
        top_indices = cosine_scores.topk(k=min(5,len(sentences))).indices
        raw_summary = '. '.join(sentences[i] for i in top_indices) + '.'
        
        #refinedsummary
        refined_summary = refine_summary_with_llm(raw_summary, query)
        
        return {"summary": f"Generating a summarized text:\n\n {refined_summary}"}
    except Exception as e:
        return {"summary": f"Summarization failed: {str(e)}"}
 
