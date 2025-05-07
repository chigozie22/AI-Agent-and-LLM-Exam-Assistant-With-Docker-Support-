from llama_cpp import Llama

llm = Llama(model_path="models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf", n_ctx=2048)


def ask_llm(question: str, context: str) -> str:
    prompt = f"""You are a helpful and precise university examination preparation assistant. Use the following  lecture notes to answer the question asked by the student.
    
    --- LECTURE NOTES START ---
    {context}
    --- LECTURE NOTES END ---

    Now based strictly on the notes above answer the following question and do not generate your own question:

    Question: {question}

    Answer:"""

    output = llm(prompt, max_tokens=512, stop=["</s>"])
    return output["choices"][0]["text"].strip()
    