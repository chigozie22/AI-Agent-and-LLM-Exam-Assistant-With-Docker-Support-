from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os 
import pickle

# os.makedirs("data",exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")


#vector dim
EMBEDDING_DIM =384

#save the vectordb and metadata
VEC_INDEX_PATH = "/home/nonso/ai-multimodal-learning-project/data/faiss_index.bin"
META_PATH = "/home/nonso/ai-multimodal-learning-project/data/doc_metadata.pkl"


def load_faiss_index():
    if os.path.exists(VEC_INDEX_PATH):
        index = faiss.read_index(VEC_INDEX_PATH)
    else:
        index = faiss.IndexFlatL2(EMBEDDING_DIM)
    
    return index

def load_metadata():
    if os.path.exists(META_PATH):
        with open(META_PATH, "rb") as f:
            return pickle.load(f)
        
    return []

#save faiss index and metadata
def save_faiss_index(index):
    faiss.write_index(index,VEC_INDEX_PATH)

def save_metadata(metadata):
    with open(META_PATH,"wb") as f:
        pickle.dump(metadata, f)

#creating the embedding andstoring in chunks
def embed_and_store(text:str, doc_id:str) -> bool:
    index = load_faiss_index()
    metadata = load_metadata()

    chunks = [text[i:i+512] for i in range(0, len(text), 512)]

    embeddings = model.encode(chunks)
    index.add(np.array(embeddings))


    metadata.extend([{"doc_id": doc_id, "text": chunk} for chunk in chunks])

    save_faiss_index(index)
    save_metadata(metadata)

    print(f"[INFO] Saved {len(chunks)} chunks to FAISS and metadata.")

    print("[DEBUG] Checking if FAISS index was saved...")
    print("FAISS exists?", os.path.exists("data/faiss_index.bin"))
    print("Metadata exists?", os.path.exists("data/doc_metadata.pkl"))

    return True

#searching for similar chunks
def search_similar_chunks(query: str, top_k: int=5):
    index = load_faiss_index()
    metadata = load_metadata()

    if index.ntotal == 0:
        return [{"error": "No documents found in the vector store yet."}]
    
    #embed the query
    query_embedding = model.encode([query]).astype("float32")

    #ensure faiss doesnt ask for morethan it has
    top_k = min(top_k, index.ntotal)

    #search in the index
    D, I = index.search(np.array(query_embedding), top_k)

    results = []

    for idx in I[0]:
        if idx < len(metadata): #safety check
            results.append(metadata[idx])

    print(f"Found {len(results)} results for query: {query}")
    return results
