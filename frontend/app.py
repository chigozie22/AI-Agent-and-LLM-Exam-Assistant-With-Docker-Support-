import streamlit as st
import requests 

st.set_page_config(page_title="Smart Exam Assistant", layout="centered")


st.title("📘 Smart Exam Assistant ")
st.write("Upload lecture notes and past exam questions, then ask intelligent questions about them")

#tabs 
tabs = st.tabs(["📤 Upload", "🤖 Ask (Simple)", "📄 Generate Questions", "📑 Ask Summarizer", "🧠 Ask AI Agent"])

#upload section
with tabs[0]:
    st.header("📤 Upload Documents")
    uploaded_files = st.file_uploader("Upload Documents or Images", accept_multiple_files=True)


    if st.button("Upload"):
        for file in uploaded_files:
            files = {'file': (file.name, file.getvalue(), file.type)}
            res = requests.post("http://localhost:8000/api/upload", files=files)
            st.success(f"{file.name} upload successfully ✅" if res.ok else "❌ Upload Failed")

#ask question non agent
with tabs[1]:
    st.header("Ask a question non agent")
    query = st.text_input("Type your question here:")

    if st.button("Ask"):
        res = requests.post("http://localhost:8000/api/ask", json={"query": query})
        if res.ok:
            st.success("Answer:")
            st.write(res.json()["answer"])
        else:
            st.error("Something went wrong")

#Generate future questions 
with tabs[2]:
    st.header("Generate likely exam questions")
    lecture_files = st.file_uploader("Upload lecture notes (PDF Or Image)", type=["pdf", "png", "jpg", "jpeg"])
    past_qsts = st.file_uploader("Upload past questions (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])

    num_questions = st.number_input("Number of Questions to Generate", min_value=1, max_value=20,value=5)

    if lecture_files and past_qsts and st.button("Generate Questions") is not None:
        with st.spinner("Generating Questions..."):
            docs = {
            "notes": (lecture_files.name, lecture_files.getvalue(), lecture_files.type),
            "past_questions":(past_qsts.name, past_qsts.getvalue(), past_qsts.type)
            }
            data = {"num_questions": str(num_questions)}
            res = requests.post(
                "http://localhost:8000/api/generate-questions-without-agent", 
                files=docs,
                data=data)
            try:
                if res.status_code ==200:
                    questions = res.json().get("generated_questions", [])
                    st.success("Generate questions:")
                    st.write(questions)
                    # for i,q in enumerate(questions,1):
                    #     st.markdown(f"**{i}. {q}**")
            
                else:
                    st.error(f"Error: {res.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")


#summarizer tab
with tabs[3]:
    st.header("🧠 Get a Summary on a concept")
    lecture_file_for_summary = st.file_uploader("Upload a lecture note to summarize", type=["pdf", "png","jpg", "jpeg", "docx"])
    summary_query = st.text_area("Input a concept you would love to get a summary on:")
    
    if lecture_file_for_summary and summary_query:
        if st.button("Summarize"):
            with st.spinner("Summarizing..."):
                files = {
                    "notes": (lecture_file_for_summary.name,
                        lecture_file_for_summary.getvalue(),
                        lecture_file_for_summary.type
                        )}
                data = {"query": summary_query}
                try:
                    res = requests.post("http://localhost:8000/api/summarize", files=files, data=data)

                    if res.status_code==200:
                        summary = res.json()["summary"]                    
                        st.success("Here is your summary: ")
                        st.write(summary)
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")



#--AI agent tab ---
with tabs[4]:
    st.header("🤖 Ask the LangGraph AI Agent")
    user_query = st.text_area("Ask me anything based on the uploaded content:")
    #file upload 
    agent_lecture_file = st.file_uploader("Upload your lecture notes for the agent to process", type=["pdf", "png","jpg", "jpeg", "docx"], key="agent_lecture_files")
    past_questions_input = st.text_area("Past Questions {if you have the need,put in the text here}", "")

    if agent_lecture_file and user_query and st.button("Ask AI Agent"):
        with st.spinner("Agent Processing..."):
            try:
                files = {
                    "lecture_file": (
                    agent_lecture_file.name, 
                    agent_lecture_file.getvalue(),
                    agent_lecture_file.type
                )
            
            }
                data = {
                    "query": user_query,
                    "past_questions": past_questions_input
                }
                res = requests.post("http://localhost:8000/invoke-agent", files=files,data=data)
                if res.status_code == 200:
                    # output = res.json().get("response", "No output received.")
                    st.success("Agent Response")
                    st.write(res.json()["response"])
                else:
                    st.error(f"Agent Error: {res.text}")

            except Exception as e:
                st.error(f"Connection error: {e}")

