import os
import sqlite3
import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
from huggingface_hub import InferenceClient

# --- Streamlit Setup ---
st.set_page_config(page_title="📊 ITC Financial AI Assistant", layout="wide")
st.title("📈 ITC Financial Analysis with LLaMA-3")

# --- API Key Input ---
hf_token = st.text_input("🔐 Enter your Hugging Face API Key:", type="password")

# --- File Paths & Constants ---
DB_PATH = 'database/document_metadata.db'
CHROMA_DIR = 'embeddings/chroma_embeddings'
COLLECTION_NAME = "itc_financial_data"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "meta-llama/Llama-3.3-70B-Instruct"

# --- Check Files Exist ---
if not os.path.exists(CHROMA_DB_FILE) or not os.path.exists(SQLITE_DB_FILE):
    st.error("❌ Required files not found. Please make sure 'chroma.sqlite3' and 'document_metadata.db' exist.")
    st.stop()

# --- Connect to SQLite ---
conn = sqlite3.connect(SQLITE_DB_FILE)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS document_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER,
        file_name TEXT,
        description TEXT,
        content TEXT
    )
''')
conn.commit()

# --- Setup ChromaDB and Embeddings ---
client = chromadb.Client()
embedder = SentenceTransformer(EMBEDDING_MODEL)

# --- Check if Collection Exists ---
try:
    collection = client.get_collection(name=COLLECTION_NAME)
except Exception:
    collection = client.create_collection(name=COLLECTION_NAME)

# --- Load from SQLite and Add to Chroma if Missing ---
cursor.execute("SELECT id, year, file_name, description, content FROM document_metadata")
rows = cursor.fetchall()

existing_ids = set(collection.get(ids=None)["ids"])  # fetch all existing ids in Chroma

new_documents = []
new_metadatas = []
new_ids = []

for row in rows:
    doc_id = f"doc_{row[0]}"
    if doc_id not in existing_ids:
        new_documents.append(row[4])  # content
        new_metadatas.append({
            "year": row[1],
            "file_name": row[2],
            "description": row[3]
        })
        new_ids.append(doc_id)

if new_documents:
    collection.add(
        documents=new_documents,
        metadatas=new_metadatas,
        ids=new_ids
    )

# --- Prompt Builder ---
def build_prompt_with_context(query, n_results=3):
    embedding = embedder.encode(query)
    results = collection.query(query_embeddings=[embedding], n_results=n_results)

    if not results['documents'][0]:
        return None, None

    context = "\n\n".join(results['documents'][0])
    prompt = (
        f"Objective: Analyze ITC’s revenue trends, profitability, and financial health using AI-scraped data and LLM insights.\n\n"
        f"You are a helpful and professional AI financial analyst. Based on the following financial data, answer the user's question with clear, insightful, and accurate information. "
        f"If specific data is missing, provide general insights or suggest next steps.\n\n"
        f"Context:\n{context}\n\n"
        f"User's Question: {query}\n\n"
        f"Answer:"
    )
    return prompt, context

# --- Hugging Face LLaMA-3 Inference ---
def get_llama_response(prompt, token):
    client = InferenceClient(api_key=token, provider="hf-inference")
    try:
        completion = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message['content']
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- User Query ---
query = st.text_input("💬 Ask your question about ITC financials:")

if st.button("Submit"):
    if not query:
        st.warning("Please enter a query.")
    elif not hf_token:
        st.warning("Please enter your Hugging Face API key.")
    else:
        # Hide unnecessary details behind the scenes
        with st.spinner("Processing your query..."):
            prompt, context = build_prompt_with_context(query)
            if not context:
                st.error("❌ No relevant context found in vector database.")
            else:
                response = get_llama_response(prompt, hf_token)
                st.subheader("📌 Answer")
                st.write(response)

                # Show context only in expanded section
                with st.expander("📂 Show Retrieved Context"):
                    st.text_area("Context from ChromaDB", context, height=300)
