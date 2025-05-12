import chromadb
from sentence_transformers import SentenceTransformer
from huggingface_hub import InferenceClient

# STEP 1: Initialize the ChromaDB client
persist_directory = 'embeddings\chroma_embeddings\chroma.sqlite3'
client = chromadb.PersistentClient(path=persist_directory)

# STEP 2: Try to get the collection, or create it if not found
collection_name = "itc_financial_data"
try:
    collection = client.get_collection(collection_name)
except chromadb.errors.NotFoundError:
    print(f"Collection '{collection_name}' not found. Creating a new one.")
    collection = client.create_collection(collection_name)


# STEP 3: Initialize the SentenceTransformer model for query embedding
query_model = SentenceTransformer('all-MiniLM-L6-v2')

# STEP 4: Set up Hugging Face InferenceClient with your API key and valid provider
hf_key = input("Enter your huggingace token:")
inference_client = InferenceClient(api_key=hf_key, provider="hf-inference")

# STEP 5: Function to build prompt with context
def build_prompt_with_context(query, n_results=3):
    # Get the embedding for the query
    query_embedding = query_model.encode(query).tolist()

    # Retrieve top n relevant documents
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    # Combine the retrieved documents into context
    retrieved_docs = results['documents'][0] if results['documents'] else []
    context = "\n\n".join(retrieved_docs) if retrieved_docs else "No relevant financial data found."

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

# STEP 6: Function to get LLaMA-3 answer from Hugging Face Inference API
def get_llama_response(prompt):
    completion = inference_client.chat.completions.create(
        model="meta-llama/Llama-3-70b-instruct",  # Correct model name
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message['content']

# STEP 7: Run an example query
if __name__ == "__main__":
    query = "What was ITC’s revenue in 2024?"
    prompt = build_prompt_with_context(query)
    response = get_llama_response(prompt)
    print(f"\nAnswer:\n{response}")
