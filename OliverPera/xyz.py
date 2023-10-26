import os
import sys
import pinecone
from langchain.llms import Replicate
from langchain.vectorstores import Pinecone
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain

# Replicate API token
os.environ['REPLICATE_API_TOKEN'] = "r8_Qn8wiPqHaURZ47yhALpPo306LzLTcAM2FAp3G"

# Initialize Pinecone

# Load and preprocess the PDF document
loader = PyPDFLoader('/Users/oliverpera/Desktop/Studium DHBW/Content/5. Semester/Projekt/talk_to_a_law/data_source/2023-06-09-erlaeuterungen-data.pdf')
documents = loader.load()

# Split the documents into smaller chunks for processing
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# Use HuggingFace embeddings for transforming text into numerical vectors
embeddings = HuggingFaceEmbeddings()

# Set up the Pinecone vector database
pinecone.init(api_key='d85317f9-1855-45b4-9e44-78bfe8088ae2', environment='gcp-starter')
index_name = "olptest"
index = pinecone.Index(index_name)
vectordb = Pinecone.from_documents(texts, embeddings, index_name=index_name)