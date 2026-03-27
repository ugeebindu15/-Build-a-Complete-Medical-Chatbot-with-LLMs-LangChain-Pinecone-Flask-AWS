from src.helper import load_pdf_Files, filter_to_minimal_doc, text_split, download_embeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

# Load and process PDF
extracted_data = load_pdf_Files("data")
minimal_docs = filter_to_minimal_doc(extracted_data)
texts_chunk = text_split(minimal_docs)
embedding = download_embeddings()

# Connect to Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medicalbot"

# Create index if not exists
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Upload embeddings to Pinecone
docsearch = PineconeVectorStore.from_documents(
    documents=texts_chunk,
    embedding=embedding,
    index_name=index_name
)

