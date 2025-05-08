!pip install tavily-python
!pip install langchain

import os
from langchain.docstore.document import Document
from google.colab import userdata
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle
from langchain.docstore.document import Document

import nltk
nltk.download('punkt')
nltk.download('stopwords')
tav_key = userdata.get('tavai')

os.environ["TAVILY_API_KEY"] = tav_key
from tavily import TavilyClient
client = TavilyClient(api_key=tav_key)


# ITC reports and accounts
pdf_sources = [
     {
         "url" : "https://www.itcportal.com/about-itc/shareholder-value/annual-reports/itc-annual-report-2024/pdf/ITC-Report-and-Accounts-2024.pdf",
        "metadata" : {
            "year" : 2024,
            "company":"ITC",
            "report type":"Annual Report",
            "file_name":"ITC-Report-and-Accounts-2024.pdf",
            "source_website":"www.itcportal.com",
            "description":"ITC's Annual Report for the financial year 2024"
        }
    },
               
    {
        "url" : "https://www.itcportal.com/about-itc/shareholder-value/annual-reports/itc-annual-report-2023/pdf/ITC-Report-and-Accounts-2023.pdf",
        "metadata" : {
            "year" : 2023,
            "company":"ITC",
            "report type":"Annual Report",
            "file_name":"ITC-Report-and-Accounts-2023.pdf",
            "source_website":"www.itcportal.com",
            "description":"ITC's Annual Report for the financial year 2023"
        }
    },

    # FAQ
    {
        "url": "https://www.itcportal.com/about-itc/shareholder-value/key-financials/q3fy25results-faq.pdf",
        "metadata": {
            "year": 2025,
            "company": "ITC",
            "report type": "FAQ Report",
            "file_name": "q3fy25results-faq.pdf",
            "source_website": "www.itcportal.com",
            "description": "FAQ related to Q3 FY25 financial results"
        }
    },
     
    {
        "url": "https://www.itcportal.com/about-itc/shareholder-value/key-financials/q2fy25results-faq.pdf",
        "metadata": {
            "year": 2025,
            "company": "ITC",
            "report type": "FAQ Report",
            "file_name": "q2fy25results-faq.pdf",
            "source_website": "www.itcportal.com",
            "description": "FAQ related to Q2 FY25 financial results"
        }
    },
     
    {
        "url": "https://www.itcportal.com/about-itc/shareholder-value/key-financials/q1fy25results-faq.pdf",
        "metadata": {
            "year": 2025,
            "company": "ITC",
            "report type": "FAQ Report",
            "file_name": "q1fy25results-faq.pdf",
            "source_website": "www.itcportal.com",
            "description": "FAQ related to Q1 FY25 financial results"
        }
    }
    

    # Press release
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Press-Release-Q1-FY2024.pdf",
        "metadata": {
            "year": 2024,
            "company": "ITC",
            "report type": "Press release Report",
            "file_name": "ITC-Press-Release-Q1-FY2024.pdf",
            "source_website": "www.itcportal.com",
            "description": "press release about Q1 FY 2024"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Press-Release-Q2-FY2024.pdf",
        "metadata": {
            "year": 2024,
            "company": "ITC",
            "report type": "Press release Report",
            "file_name": "ITC-Press-Release-Q2-FY2024.pdf",
            "source_website": "www.itcportal.com",
            "description": "press release about Q2 FY 2024"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Press-Release-Q3-FY2024.pdf",
        "metadata": {
            "year": 2024,
            "company": "ITC",
            "report type": "Press release Report",
            "file_name": "ITC-Press-Release-Q3-FY2024.pdf",
            "source_website": "www.itcportal.com",
            "description": "press release about Q3 FY 2024"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Press-Release-Q4-FY2024.pdf",
        "metadata": {
            "year": 2024,
            "company": "ITC",
            "report type": "Press release Report",
            "file_name": "ITC-Press-Release-Q4-FY2024.pdf",
            "source_website": "www.itcportal.com",
            "description": "press release about Q4 FY 2024"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Press-Release-Q4-FY2023.pdf",
        "metadata": {
            "year": 2023,
            "company": "ITC",
            "report type": "Press release Report",
            "file_name": "ITC-Press-Release-Q4-FY2023.pdf",
            "source_website": "www.itcportal.com",
            "description": "press release about Q4 FY 2023"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Press-Release-Q3-FY2023.pdf",
        "metadata": {
            "year": 2023,
            "company": "ITC",
            "report type": "Press release Report",
            "file_name": "ITC-Press-Release-Q3-FY2023.pdf",
            "source_website": "www.itcportal.com",
            "description": "press release about Q3 FY 2023"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Press-Release-Q2-FY2023.pdf",
        "metadata": {
            "year": 2023,
            "company": "ITC",
            "report type": "Press release Report",
            "file_name": "ITC-Press-Release-Q2-FY2023.pdf",
            "source_website": "www.itcportal.com",
            "description": "press release about Q2 FY 2023"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Press-Release-Q1-FY2023.pdf",
        "metadata": {
            "year": 2023,
            "company": "ITC",
            "report type": "Press release Report",
            "file_name": "ITC-Press-Release-Q1-FY2023.pdf",
            "source_website": "www.itcportal.com",
            "description": "press release about Q1 FY 2023"
        }
    }

    
    # Standalone
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Financial-Result-Q4-FY2024-sfs.pdf",
        "metadata": {
            "year": 2024,
            "company": "ITC",
            "report type": "Standalone Report",
            "file_name": "ITC-Financial-Result-Q4-FY2024-sfs.pdf",
            "source_website": "www.itcportal.com",
            "description": "Standalone about Q4 FY 2024"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Financial-Result-Q3-FY2024-sfs.pdf",
        "metadata": {
            "year": 2024,
            "company": "ITC",
            "report type": "Standalone Report",
            "file_name": "ITC-Financial-Result-Q3-FY2024-sfs.pdf",
            "source_website": "www.itcportal.com",
            "description": "Standalone about Q3 FY 2024"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Financial-Result-Q2-FY2024-sfs.pdf",
        "metadata": {
            "year": 2024,
            "company": "ITC",
            "report type": "Standalone Report",
            "file_name": "ITC-Financial-Result-Q2-FY2024-sfs.pdf",
            "source_website": "www.itcportal.com",
            "description": "Standalone about Q2 FY 2024"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Financial-Result-Q1-FY2024-sfs.pdf",
        "metadata": {
            "year": 2024,
            "company": "ITC",
            "report type": "Standalone Report",
            "file_name": "ITC-Financial-Result-Q1-FY2024-sfs.pdf",
            "source_website": "www.itcportal.com",
            "description": "Standalone about Q1 FY 2024"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Financial-Result-Q4-FY2023-sfs.pdf",
        "metadata": {
            "year": 2023,
            "company": "ITC",
            "report type": "Standalone Report",
            "file_name": "ITC-Financial-Result-Q4-FY2023-sfs.pdf",
            "source_website": "www.itcportal.com",
            "description": "Standalone about Q4 FY 2023"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Financial-Result-Q3-FY2023-sfs.pdf",
        "metadata": {
            "year": 2023,
            "company": "ITC",
            "report type": "Standalone Report",
            "file_name": "ITC-Financial-Result-Q3-FY2023-sfs.pdf",
            "source_website": "www.itcportal.com",
            "description": "Standalone about Q3 FY 2023"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Financial-Result-Q2-FY2023-sfs.pdf",
        "metadata": {
            "year": 2023,
            "company": "ITC",
            "report type": "Standalone Report",
            "file_name": "ITC-Financial-Result-Q2-FY2023-sfs.pdf",
            "source_website": "www.itcportal.com",
            "description": "Standalone about Q2 FY 2023"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Financial-Result-Q1-FY2023-sfs.pdf",
        "metadata": {
            "year": 2023,
            "company": "ITC",
            "report type": "Standalone Report",
            "file_name": "ITC-Financial-Result-Q1-FY2023-sfs.pdf",
            "source_website": "www.itcportal.com",
            "description": "Standalone about Q1 FY 2023"
        }
    },

    # Consolidated
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Financial-Result-Q4-FY2024-cfs.pdf",
        "metadata": {
            "year": 2024,
            "company": "ITC",
            "report type": "Consolidated Report",
            "file_name": "ITC-Financial-Result-Q4-FY2024-cfs.pdf",
            "source_website": "www.itcportal.com",
            "description": "Consolidated about Q4 FY 2024"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Financial-Result-Q3-FY2024-cfs.pdf",
        "metadata": {
            "year": 2024,
            "company": "ITC",
            "report type": "Consolidated Report",
            "file_name": "ITC-Financial-Result-Q3-FY2024-cfs.pdf",
            "source_website": "www.itcportal.com",
            "description": "Consolidated about Q3 FY 2024"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Financial-Result-Q2-FY2024-cfs.pdf",
        "metadata": {
            "year": 2024,
            "company": "ITC",
            "report type": "Consolidated Report",
            "file_name": "ITC-Financial-Result-Q2-FY2024-cfs.pdf",
            "source_website": "www.itcportal.com",
            "description": "Consolidated about Q2 FY 2024"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Financial-Result-Q1-FY2024-cfs.pdf",
        "metadata": {
            "year": 2024,
            "company": "ITC",
            "report type": "Consolidated Report",
            "file_name": "ITC-Financial-Result-Q1-FY2024-cfs.pdf",
            "source_website": "www.itcportal.com",
            "description": "Consolidated about Q1 FY 2024"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Financial-Result-Q1-FY2023-cfs.pdf",
        "metadata": {
            "year": 2023,
            "company": "ITC",
            "report type": "Consolidated Report",
            "file_name": "ITC-Financial-Result-Q1-FY2023-cfs.pdf",
            "source_website": "www.itcportal.com",
            "description": "Consolidated about Q1 FY 2023"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Financial-Result-Q2-FY2023-cfs.pdf",
        "metadata": {
            "year": 2023,
            "company": "ITC",
            "report type": "Consolidated Report",
            "file_name": "ITC-Financial-Result-Q2-FY2023-cfs.pdf",
            "source_website": "www.itcportal.com",
            "description": "Consolidated about Q2 FY 2023"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Financial-Result-Q3-FY2023-cfs.pdf",
        "metadata": {
            "year": 2023,
            "company": "ITC",
            "report type": "Consolidated Report",
            "file_name": "ITC-Financial-Result-Q3-FY2023-cfs.pdf",
            "source_website": "www.itcportal.com",
            "description": "Consolidated about Q3 FY 2023"
        }
    },
    {
        "url": "https://www.itcportal.com/investor/pdf/ITC-Financial-Result-Q4-FY2023-cfs.pdf",
        "metadata": {
            "year": 2023,
            "company": "ITC",
            "report type": "Consolidated Report",
            "file_name": "ITC-Financial-Result-Q4-FY2023-cfs.pdf",
            "source_website": "www.itcportal.com",
            "description": "Consolidated about Q4 FY 2023"
        }
    }
]

doc = []
for pdf in pdf_sources:
    response = client.extract(urls=pdf["url"], extract_depth="advanced")
    if response['results']:
        content = response['results'][0]['raw_content']
        doc.append(Document(page_content=content, metadata=pdf["metadata"]))



# Define a simple cleaning function
def clean_text(text):
    # Convert text to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    # Remove numbers (optional)
    text = re.sub(r'\d+', '', text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    
    # Recreate text from filtered tokens
    return " ".join(filtered_text)

# Initialize the list of documents
cleaned_documents = []

# Loop through the pdf_sources (your scraped data)
for pdf in pdf_sources:
    response = client.extract(urls=pdf["url"], extract_depth="advanced")
    
    if response['results']:
        content = response['results'][0]['raw_content']
        
        # Clean the content
        cleaned_content = clean_text(content)
        
        # Extract title from metadata (using file_name as the title in this case)
        title = pdf["metadata"].get("file_name", "No Title")
        
        # Create a Document object with cleaned content and metadata
        document = Document(page_content=cleaned_content, metadata=pdf["metadata"])
        cleaned_documents.append(document)
        
    else:
        print(f"No results found for {pdf['url']}")

# Save the cleaned documents into a pickle file
pickle_path = '/content/scraped_documents.pkl'
with open(pickle_path, 'wb') as file:
    pickle.dump(doc, file)

print(f"Documents saved to {pickle_path}")
