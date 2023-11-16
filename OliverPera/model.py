from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from transformers import AutoModelForCausalLM


db_source_path = "faiss_index" 

prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

def set_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    
    prompt = PromptTemplate(template=prompt_template,
                            input_variables=['context', 'question']
                            )
    
    return prompt

def create_question_answer_chain(llm, prompt, db):
    question_answer_chain = RetrievalQA.from_chain_type(llm=llm,
                                       return_source_documents=True,
                                       retriever=db.as_retriever(search_kwargs={'k': 2}),
                                       chain_type_kwargs={'prompt': prompt},
                                       chain_type='stuff',
                                       )
    
    return question_answer_chain

def load_llm():
    llm = CTransformers(
        model = "llama-2-7b-chat.ggmlv3.q8_0.bin", ##"llama-2-7b-chat.ggmlv3.q8_0.bin", ##AutoModelForCausalLM.from_pretrained("jphme/Llama-2-13b-chat-german"),
        model_type="llama",
        temperature = 0.5,
        max_new_tokens = 512,
        )
    
    return llm

def execute_bot():
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {'device': 'cpu'}
    embeddings = HuggingFaceEmbeddings(model_name=model_name, 
                                       model_kwargs=model_kwargs)
    
    db = FAISS.load_local(db_source_path, embeddings)
    llm = load_llm()
    
    question_answer_prompt = set_prompt()
    question_answer = create_question_answer_chain(llm, question_answer_prompt, db)

    return question_answer

