from llama_cpp import Llama

llm = Llama(model_path="models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf", n_ctx=10000)



def generate_possible_questions(notes: str, past_questions: str, num_question: int) -> str:
    prompt = f"""
    You are an intelligent and precise university examination preparation assistant and tutor. 
    Based on the lecture notes and the academic style of the previous exam questions.
    generate {num_question} likely future exam quesitons.

    --Example past questions---
    1. Sketch the electronic circuit of a Klystron tube and write short note on: (i.) Velocity modulation, (ii.) Bunching process.
    2. Derive the velocity modulation equation V(t) of a Klystron tube.
    3. A 2-Cavity Klystron operates at 4.5GHz with...


    --- LECTURE NOTES ---
    {notes[:3000]}
    --- PAST QUESTIONS ---
    {past_questions[:2000]}

    Only output the generated questions, number them according to the
    numbering style in the previous examination questions. """

    output = llm(prompt, max_tokens=512, temperature=0.7, stop=["\n\n"])

    return output["choices"][0]["text"]