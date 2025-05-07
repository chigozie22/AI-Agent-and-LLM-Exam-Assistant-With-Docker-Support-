from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode 
from langchain_core.tools import tool 
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_models import ChatLlamaCpp 
from langchain_unstructured import UnstructuredLoader
from pydantic import BaseModel 
from langchain_core.runnables import RunnableLambda
from typing import List, Optional 
import tempfile

#llm 
llm = ChatLlamaCpp(
    model_path="/home/nonso/ai-multimodal-learning-project/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
    temperature=0.5,
    max_tokens=2048,
    context_window=10000,
    streaming=False
)

# === Shared Memory State ===
class AgentState(BaseModel):
    messages: List[HumanMessage]
    lecture_filename: Optional[str] = None
    lecture_file_content: Optional[bytes] = None
    past_question_text: Optional[str] = None
    extracted_text: Optional[str] = None
    extracted_lecture_text: Optional[str] = None
    query: Optional[str] = None
    result: Optional[str] = None
    

    class Config:
        arbitrary_types_allowed = True


#file extractor 
@tool
def extract_text(filename: str, file_content: bytes) -> str:
    """
    Extracts text from a file (PDF, DOCX, or Image)

    """
    try: 
        with tempfile.NamedTemporaryFile(delete=False
                                         , suffix="." + filename.split(".")[-1]) as f:
            f.write(file_content)
            temp_path = f.name
        loader = UnstructuredLoader(temp_path)
        docs = loader.load()
        text = "\n".join(docs.page_content for doc in docs)
    
        if len(text) > 10000:
            print("Extracted text istoo long, truncating...")
            return text[:10000]
        
        return text

    except Exception as e:
        return f"Error extracting text: {e}"
    
#binding thetool 
tools =[extract_text]
tool_node = ToolNode([extract_text])

# model_with_tools = llm.bind_tools(tools)

#graph node to extract lecture notes text
def chatbot_extract_node(state: AgentState) -> AgentState:
    extracted_text = extract_text.invoke({
        "filename": state.lecture_filename,
        "file_content": state.lecture_file_content
    })
    state.extracted_lecture_text = extracted_text
    return state
   

#node to reason
def llm_reasoning_node(state: AgentState) -> AgentState:
    if not state.messages:
        state.result = "No task was provided. Please send a message with your request."
        return state
    
    
    query = state.messages[-1].content.lower()
    
    #shorten lecture notes to avoid token overflow
    lecture_text = state.extracted_lecture_text or ""
    if len(lecture_text) >3000:
        lecture_text = lecture_text[:3000] + "\n\n[...truncated for context limit]"

    if "summarize" in query:
        prompt = f"""
        You are an expert academic tutor.
        Use the lectures notes summarize a specific concept or topic in the student's request

    Lecture Notes:
    {lecture_text}

    Students's Request:
    {query}

    Please provided a comprehensive, focused and consise summary.
    """
        
    elif "generate" in query or "exam question" in query:
        past_qs = state.past_question_text or "(None Provided)"
        prompt = f""" Your are an expert academic examniation assistant. Use the lecture notes and past questions below to generate likely exam questions.
    
    Lecture Notes:
    {lecture_text[:3000]}

    Past Exam Questions:
    {past_qs[:1000]}
    
    """
    else:
        #Default to question answering 
        prompt= f"""You are an expert academic assistant. Use the lecture note below to answer the following quesitons:

    Lecture notes:
    {lecture_text}

    Question:
    {query}
    """

    try:
        response = llm.invoke(prompt)
        state.result = response.content
    except Exception as e:
        state.result = f"LLM Error: {str(e)}"

    return state

#graph struture 
graph_builder = StateGraph(AgentState)


graph_builder.add_node("extract", chatbot_extract_node)
# graph_builder.add_node("chat", tool_node.bind())

graph_builder.add_node("llm_reasoning", RunnableLambda(llm_reasoning_node))

# graph_builder.add_edge(    njmh, "extract")
graph_builder.set_entry_point("extract")
# graph_builder.add_edge("extract", "chat")
graph_builder.add_edge("extract", "llm_reasoning")
graph_builder.add_edge("llm_reasoning", END)

graph = graph_builder.compile()



# file_path = "/home/nonso/Downloads"

# lecture_note = "/home/nonso/Downloads/ECE 502 Microwave Amplifiers.pdf"

# with open(lecture_note, "rb") as f:
#     lecture_bytes = f.read()

# past_questions = """
# 1. Sketch the electronic circuit of a Klystron tube and write short note on: (i.) Velocity modulation, ii. Bunching process
# 2. . Derive the velocity modulation equation V(t) of a Klystron tube (5 marks)
#      A 2-Cavity Klystron operates at 4.5GHz with a dc voltage of 9.2KV and a 1.5mm cavity gap. For a given RF voltage, the magnitude of gap voltage is 105volts. Calculate; (a.) Transit angle (b.) min/max-Velocity of electron leaving the gap 
# 3. Sketch and describe, the operation of a Travelling Wave Tube (TWT), in not more than 10 lines 
# 4. State 4 characteristics of a TWT and 3 areas of application, respectively 
# 5  A helical travelling wave tube with a circumference to pitch ratio of 10 operates at 3.5GHz under a beam voltage is 5KV and beam current is 30mA. If the helix impedance is 120 Ohm and circuit length N=35; Determine the anode voltage of which the TWT can be operated for any useful gain. Find the output power gain. 
# 6. In the operation of a Magnetron, state 4 forces that affect electrons gyrations 
# 7. Outline the 4 types of Anode cavity design of a Magnetron. 
# 8. Briefly explain with a sketch, high gain and high bandwidth operations, of a Magnetron 
# 9. State mathematically, the condition for maximum power transfer, in the operation of magnetron (6marks)
# 10. (c) Mathematically deduce; (i) the cut off magnetic field (BC) of a Magnetron, and (ii) the maximum angular velocity (w) of the electron bunch in magnetron. (7marks)
# ...
# """

def run_agent(lecture_file: bytes, lecture_filename: str, query:str, past_questions: str="") -> str:
    from langchain_core.messages import HumanMessage

    input_state = {
        "messages": [HumanMessage(content=query)],  
        "lecture_file_content": lecture_file,         
        "lecture_filename": lecture_filename,
        "past_question_text": past_questions,
    }

    #run the graph

    final_state = graph.invoke(input_state)

    print("===Result===")
    return final_state["result"]