from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 

def create_faiss_vector_db(data_source_path, db_target_path):
    data = DirectoryLoader(data_source_path, 
                           loader_cls=PyPDFLoader, 
                           glob='*.pdf')
    documents = data.load()
    
    char_text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, 
                                                        chunk_overlap = 50) ## tuning parameter
    texts = char_text_splitter.split_documents(documents)
    
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {'device': 'cpu'}
    embeddings = HuggingFaceEmbeddings(model_name=model_name,
                                       model_kwargs=model_kwargs)
    
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(db_target_path)

    
if __name__ == "__main__":
    
    data_source_path = "data_source/"
    db_target_path = "OliverPera/faiss_index"   
    
    create_faiss_vector_db(data_source_path, db_target_path)
    