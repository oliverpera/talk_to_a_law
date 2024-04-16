from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from transformers import AutoModelForCausalLM
import replicate


system_prompt = "Du bist ein verständlicher Assistent. Du hast Zugriff auf eine Wissensdatenbank für das Deutsche Bankrecht und kannst Fragen beantworten. Die Fragen sollen für Personen ohne Erfahrung verständlich sein"

def execute_bot(message: str):
    
    prompt = set_prompt(message,False)
    question_answer = replicate.run(
        "mistralai/mixtral-8x7b-instruct-v0.1",
        input={
            "prompt": prompt,
            "system_prompt": system_prompt,
            "max_new_tokens": 1024
        },
    )
    
    return "".join(question_answer)


def set_prompt(message,useDB):
    if useDB == True:
    
    else:
        prompt = message 
        return prompt 


