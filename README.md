# 💼Unlock ITC’s Financial Data with AI-Powered Query Analysis

A complete AI-powered system to analyze ITC Ltd.'s financial reports, investor presentations, and stock price history. The system enables natural language Q&A with **source citation** and provides **semantic search** over all collected documents using embeddings.

---

## 🚀 Key Features

- ✅ **Data scraping** (annual reports, investor presentations, stock price history)
- ✅ **Document embeddings** for semantic search
- ✅ **Natural language Q&A** powered by LLMs
- ✅ **Source citation** in every answer
- ✅ Easy-to-use **Streamlit app interface**
- ✅ **Secure Hugging Face token entry** (no token is stored in the code)

---

## 📥 Data Collection

The data collection process gathers ITC Ltd.’s **financial reports, investor presentations, and stock price history** to build a rich dataset.

### 🔑 Tavily API

I used the **Tavily API** to scrape reports and presentations directly from ITC’s investor relations website.

**Steps:**

1️⃣ Get your own **Tavily API key:**  
➡️ [https://www.tavily.com/](https://www.tavily.com/)

2️⃣ Use the API key in the scraping script (you’ll be securely prompted to enter it).

**Scraping script:**  
👉 [`data_scraper.py`](./data_scraper.py)

The script fetches:

- 🗂 **Annual reports** (PDFs)
- 🗂 **Investor presentations**
- 📈 **Stock price history**

### 🗄️ Database Setup

A **SQLite database** is used to store metadata and extracted document text.

**Database table schema:**

    ```sql
    CREATE TABLE IF NOT EXISTS document_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER,
        file_name TEXT,
        description TEXT,
        content TEXT
    );




# **Document Embedding and Querying with ChromaDB and Hugging Face's Llama-3.3-70B-Instruct**

## **Overview**

In this approach, we leverage two powerful tools: **Sentence Transformers** for document embedding and **ChromaDB** for storing these embeddings in a vector database. The embeddings are used to enable semantic search and retrieval of relevant documents. For querying, we use the **Llama-3.3-70B-Instruct** model from **Hugging Face**, which generates natural language responses based on the embedded content.

## **Sentence Transformers for Document Embeddings**

### **What are Embeddings?**

Embeddings are dense vector representations of text that capture the semantic meaning of words, sentences, or documents. By converting text into embeddings, we allow the system to understand the content in a form that can be mathematically compared and searched.

**Sentence Transformers** is a popular library for generating sentence-level embeddings. It takes a piece of text and converts it into a fixed-size vector of numbers that captures the meaning of that text.

### **Why Sentence Transformers?**

Sentence Transformers provide high-quality embeddings that allow us to:
- **Compare texts** by calculating the cosine similarity between embeddings.
- **Cluster similar documents** and perform tasks like search and classification efficiently.

In our case, we use a pre-trained Sentence Transformer model such as `all-MiniLM-L6-v2`, which is known for its efficiency and accuracy in generating embeddings for short texts and documents.

## **ChromaDB for Storing Embeddings**

### **What is ChromaDB?**

ChromaDB is a vector database that allows you to store and search for embeddings in a highly optimized way. By using ChromaDB, we can store the embeddings of documents and then perform efficient similarity searches over large datasets.

### **How ChromaDB Works?**

- **Document Insertion:** After generating embeddings for documents using Sentence Transformers, ChromaDB stores the embeddings along with metadata like the document’s title, year, or any other relevant information.
- **Querying:** When a user submits a query, we also embed the query text into a vector and search for the most similar document embeddings in the database. ChromaDB returns the documents that are semantically most relevant to the query.

### **Why ChromaDB?**

ChromaDB offers several advantages for handling embeddings:
- It provides a **fast** and **scalable** solution for vector searches.
- It stores both the vector embeddings and metadata, enabling rich searches with context.

## **Hugging Face’s Llama-3.3-70B-Instruct for Querying**

### **What is Llama-3.3-70B-Instruct?**

Llama-3.3-70B-Instruct is a state-of-the-art transformer model from **Hugging Face** that is fine-tuned for instruction-based tasks. It excels in generating coherent, natural language responses to user queries. 

### **Why Use Llama for Querying?**

Llama is designed to handle complex language tasks:
- **Interpret complex queries**: It can understand user input and interpret queries in a natural, conversational manner.
- **Generate answers**: Based on the embedded documents, Llama can generate responses that are more contextually accurate and coherent.

### **How Llama Helps in this Pipeline?**

After retrieving the most relevant document embeddings from ChromaDB, we pass the results to the Llama-3.3-70B-Instruct model. Llama processes the input and generates human-readable text in response to the query, making it easier to extract meaningful insights from a large dataset.

## **End-to-End Workflow**

1. **Embedding Documents:** Documents are first converted into embeddings using **Sentence Transformers**, capturing their semantic meaning.
2. **Storing Embeddings:** These embeddings, along with metadata (such as year, file name), are stored in **ChromaDB** for efficient retrieval.
3. **Querying with Llama:** When a user submits a query, we convert the query into an embedding and search for the closest document embeddings in **ChromaDB**.
4. **Generating Response:** The relevant documents are passed to the **Llama-3.3-70B-Instruct** model, which generates a coherent response based on the content of those documents.

## **Conclusion**

This approach combines powerful tools to process, store, and query large sets of documents. By using **Sentence Transformers** and **ChromaDB** for document embeddings and storage, coupled with **Llama-3.3-70B-Instruct** for natural language querying, this solution provides an efficient, scalable way to analyze and retrieve information from unstructured text data.

With this architecture, you can perform semantic search, retrieve relevant documents, and generate meaningful responses for your queries, all powered by cutting-edge machine learning models and optimized database technologies.

---

## 🛠️ Tech Stack

- Python 3.10+
- Streamlit
- ChromaDB
- Hugging Face Transformers
- LangChain
- FAISS
- Pydantic
- Other supporting libraries (see `requirements.txt`)

---

## 🔧 Installation & Setup

1️⃣ **Clone the repository:**

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
