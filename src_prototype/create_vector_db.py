from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from llmsherpa.readers import LayoutPDFReader
import os
from llama_index.readers.schema.base import Document
from llama_index import VectorStoreIndex

def create_faiss_vector_db(data_source_path, db_target_path):
    texts_splits = []
    
    llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"
    pdf_reader = LayoutPDFReader(llmsherpa_api_url)

    # data = DirectoryLoader(data_source_path, 
    #                         loader_cls=PyPDFLoader, 
    #                         glob='*.pdf')
    
        
    # documents = pdf_reader.read_pdf(data)
    # for x in documents:
    #     print(x)
    
    pdf_folder = "../data_source"    
    
    for filename in os.listdir(pdf_folder):
        if filename[-4:].lower() == ".pdf":
            file_path = os.path.join(pdf_folder, filename)
            
            doc = pdf_reader.read_pdf(file_path)
            # for chunk in doc.chunks():
            #     text=chunk.to_context_text()
            # #     ##texts_splits.append(split.to_context_text())
            
    
    db = FAISS.from_texts(doc)
    db.save_local(db_target_path)
   
            

    # print(texts_splits)
    
    # 
    # texts = char_text_splitter.split_documents(documents)
            
    # model_name = "sentence-transformers/all-MiniLM-L6-v2"
    # model_kwargs = {'device': 'cpu'}
    # embeddings = HuggingFaceEmbeddings(model_name=model_name,
    #                                    model_kwargs=model_kwargs)
    
    # db = FAISS.from_texts(texts_splits, embeddings)
    # db.save_local(db_target_path)

    
if __name__ == "__main__":
    
    data_source_path = "data_source/"
    db_target_path = "OliverPera/faiss_index"   
    
    create_faiss_vector_db(data_source_path, db_target_path)
    