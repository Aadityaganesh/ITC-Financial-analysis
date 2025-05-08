import sqlite3
import pickle

# Load the pickle file (assuming the pickle file contains a list of Document objects)
pickle_path = '/content/scraped_documents.pkl'
with open(pickle_path, 'rb') as file:
    documents = pickle.load(file)

# Connect to SQLite3 database (it will create a new database file if it doesn't exist)
conn = sqlite3.connect('document_metadata2.db')
cursor = conn.cursor()

# Create a table to store year, file_name, description, and page_content
cursor.execute('''
CREATE TABLE IF NOT EXISTS document_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER,
    file_name TEXT,
    description TEXT,
    content TEXT
)
''')

# Insert data into the table
for document in documents:
    metadata = document.metadata
    year = metadata.get('year')
    file_name = metadata.get('file_name')
    description = metadata.get('description')
    content = document.page_content  # Accessing page content from the Document object
    
    cursor.execute('''
    INSERT INTO document_metadata (year, file_name, description, content)
    VALUES (?, ?, ?, ?)
    ''', (year, file_name, description, content))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Metadata and page content successfully stored in SQLite3 database.")
