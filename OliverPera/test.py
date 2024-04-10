from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import replicate 



def get_similar_documents(query, retriever, k=5):
    results = retriever.search(query, k=k)
    similar_documents = [result.text for result in results]
    return similar_documents

# def append_similar_documents_to_prompt(prompt, similar_documents):
#     prompt += "\n\nSimilar Documents:\n"
#     for i, doc in enumerate(similar_documents):
#         prompt += f"{i+1}. {doc}\n"
#     return prompt

# # Example usage
# query = "Was ist ein Kreditinstitut?"
# similar_documents = get_similar_documents(query, retriever)
# prompt = append_similar_documents_to_prompt(prompt, similar_documents)
        
        
        
def answer_question():
    prompt = "Was ist ein Kreditinstitut? Zeige mir die Definition aus dem Bankrecht."
    
    db_source_path = "faiss_index" 
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {'device': 'cpu'}
    embeddings = HuggingFaceEmbeddings(model_name=model_name, 
                                       model_kwargs=model_kwargs)

    db = FAISS.load_local(db_source_path, embeddings)

    retriever=db.as_retriever(search_kwargs={'k': 2})
    retrieve = retriever.invoke(prompt)
    print(len(retrieve))
    # for x in retrieve:
    #     print(x.page_content,'\n\n')



    
    docs = db.similarity_search(prompt, k=2)
    print(len(docs))
    for doc in docs:
        print(doc.page_content,'\n\n')
        


        
        
    system_prompt = "Du bist ein hilfsbereiter, freundlicher und verständlicher Assistent. Du hast Zugriff auf eine Wissensdatenbank für das Deutsche Bankrecht und kannst Fragen beantworten."
    
    iterator = replicate.run(
        "mistralai/mixtral-8x7b-instruct-v0.1",
        input={
            "prompt": prompt,
            "system_prompt": system_prompt,
            "db_source_path": db_source_path,
            "model_name": model_name,
            "model_kwargs": model_kwargs
        },
    )

    answer = ""
    
    for text in iterator:
        #print(text)
        answer += text
        
    print(answer)

    
    
answer_question()
