import sqlite3
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import shutil
from google.colab import files

conn = sqlite3.connect('/content/document_metadata2.db')
cursor = conn.cursor()

# Run query to fetch rows
query = "SELECT id, content, file_name, year, description FROM document_metadata"
cursor.execute(query)
rows = cursor.fetchall()
print(f"Fetched {len(rows)} rows.")

# Build documents
documents = [
    Document(
        page_content=row[1],
        metadata={
            "id": row[0],
            "file_name": row[2],
            "year": row[3],
            "description": row[4]
        }
    )
    for row in rows
]

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunked_docs = text_splitter.split_documents(documents)

# Embedding model (new way)
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Create Chroma vector store
persist_directory = "/content/chroma_db1"
vectorstore = Chroma.from_documents(
    documents=chunked_docs,
    embedding=embedding,
    persist_directory=persist_directory
)
vectorstore.persist()
print(f"✅ Vector store created and saved at {persist_directory}")

# Zip the vector store
zip_output_path = "/content/chroma_db1"
shutil.make_archive(zip_output_path, 'zip', persist_directory)

# Download the zip
files.download(f"{zip_output_path}.zip")
print(f"✅ Zip file {zip_output_path}.zip created and download started!")
