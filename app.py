import os
import chromadb
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from huggingface_hub import InferenceClient

# STEP 1: Initialize the ChromaDB client and load the collection
persist_directory = '/content/chroma_db1/chroma.sqlite3'  # Path to the ChromaDB database
client = chromadb.Client()

# Load the collection from ChromaDB
collection = client.get_collection("itc_financial_data")

# STEP 2: Initialize the SentenceTransformer model for query embedding
query_model = SentenceTransformer('all-MiniLM-L6-v2')

# STEP 3: Set up Hugging Face InferenceClient with your API key
from google.colab import userdata
hf_key = userdata.get('hf-itc-repo')  # Fetch Hugging Face API key from userdata
inference_client = InferenceClient(api_key=hf_key)

# STEP 4: Define the function to query ChromaDB and build the prompt
def build_prompt_with_context(query, n_results=3):
    # Get the embedding for the query
    query_embedding = query_model.encode(query)
    
    # Retrieve top n relevant documents
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    # Combine the retrieved documents into context
    retrieved_docs = results['documents'][0]  # List of top documents
    context = "\n\n".join(retrieved_docs)
    
    # Build a system prompt to instruct the LLaMA model
    prompt = (
        f"Objective: Analyze ITC’s revenue trends, profitability, and financial health using AI-scraped data and LLM insights.\n\n"
        f"You are a helpful and polite AI financial analyst. Based on the following financial data, answer the user's question with clear, insightful, and accurate information. "
        f"Always be professional, and if specific data is missing, provide general insights or suggest next steps.\n\n"
        f"Context:\n{context}\n\n"
        f"User's Question: {query}\n\n"
        f"Answer:"
    )
    
    return prompt

# STEP 5: Define the function to get an answer from Hugging Face Inference API
def get_llama_response(prompt):
    completion = inference_client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct",  # Correct model
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message['content']

# STEP 6: Example query
query = "What was ITC’s revenue in 2024?"

# Build the prompt with retrieved context from ChromaDB
prompt = build_prompt_with_context(query)

# Get the answer from the LLaMA-3 model via Hugging Face API
response = get_llama_response(prompt)

# Output the response
print(f"Answer: {response}")
