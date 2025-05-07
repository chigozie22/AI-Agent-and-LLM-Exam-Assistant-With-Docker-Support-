from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import VectorStoreRetrieverMemory
import os 

#set up embedding model 
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#directory to store persistent memory
CHROMA_DB_DIR = "backend/services/chroma_db"
# os.makedirs(CHROMA_DB_DIR, exist_ok=True)

def get_chroma_memory(session_id: str) -> VectorStoreRetrieverMemory:
    """
    Initializes or retrieves Chroma-based memory for a session
    """

    vectorestore = Chroma(
        collection_name=f"agent_memory_{session_id}",
        embedding_function=embedding_model,
        persist_directory=CHROMA_DB_DIR,
    )

    retriever = vectorestore.as_retriever()

    memory = VectorStoreRetrieverMemory(
        retriever=retriever,
        memory_key="chat_history"
    )

    return memory, retriever