
import pandas as pd
from chromadb import Documents, EmbeddingFunction, Embeddings
from prompt_templates import prompt_template, prompt_template_role_prompting, prompt_template_zero_shot, prompt_template_one_shot
from replicate import Client
from embeddings import SpacyEmbeddingsFunction
import os
import pandas as pd
import chromadb
from prompt_templates import prompt_template, prompt_template_role_prompting, prompt_template_zero_shot, prompt_template_one_shot
from replicate import Client
from embeddings import SpacyEmbeddingsFunction
import os
import spacy

replicateSession = Client()
class ReplicateEmbeddingsFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = [replicateSession.run(
            "replicate/all-mpnet-base-v2:b6b7585c9640cd7a9572c6e129c9549d79c9c31f0d3fdce7baac7c67ca38f305",
            input={"text": document},
        )[0]['embedding'] for document in input]
        return embeddings
replicate_ef = ReplicateEmbeddingsFunction()

class SpacyEmbeddingsFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        nlp = spacy.load("de_core_news_lg") # md , lg
        embeddings = [nlp(document).vector.tolist() for document in input]
        return embeddings
spacy_ef = SpacyEmbeddingsFunction()


def set_prompt(collection, question, prompt_templ):
    query_result = collection.query(
        # query_embeddings=[], # embedded question / part of question # HERE: PREFORMULATE ANSWER, EMBED ANSWER, RETRIEVE REAL KNOWLEDGE ?!? # needs to be the same dimension as embedded vectors in db
        query_texts=[question], # ALTERNATIVE THAN QUERYING WITH EMBEDDINGS -> CHROMA WILL AUTOMATICALLY EMBED USING EMBEDDING FUNCTION OF COLLECTION
        n_results=4, # number of docs to retrieve
    )
    
    documents = query_result['documents']            
    context = '\n'.join([item.replace('\xad\n', '') for document in documents for item in document])
    prompt = prompt_templ.format(query=question, context=context)
    return prompt
    
def get_collection(name):
    if name.endswith("replicate"):
        return chroma_client.get_collection(name=name) ## to check / add embedding_function=ReplicateEmbeddingsFunction()
    
    if name.endswith("spacy"):
        return chroma_client.get_collection(name=name) ## to check / add embedding_function=SpacyEmbeddingsFunction()
    
    return ValueError("Invalid embedding")

    
def set_prompt(collection, question, prompt_templ):
    query_result = collection.query(
        query_texts=[question],
        n_results=4,
    )
        
    documents = query_result['documents']            
    context = '\n'.join([item.replace('\xad\n', '') for document in documents for item in document])
    prompt = prompt_templ.format(query=question, context=context)
    return prompt

def process_question(collection, model, question, answer, prompt_template, source_qa):
    prompt = set_prompt(get_collection(collection), question, prompt_template)
            
    replicateSession = Client()
    input = {
        "prompt": prompt,
    }
        
    iterator = replicateSession.run(
        model,
        input=input,
    )
        
    answer_with_context = ''
        
    for text in iterator:
        answer_with_context += text
        
    # Write question, answer, and answer_with_context to a text file
    with open(f'/Users/oliverpera/Desktop/talk_to_a_law-1/src/app/output_{model.replace("/", "-")}.txt', 'a', encoding='utf-8') as file:
        file.write("\n")
        file.write(f"Question: {question}\n")
        file.write(f"Prompt: {prompt}\n")
        file.write(f"Answer: {answer}\n")
        file.write(f"Answer with Context: {answer_with_context}\n")
        
    return [{
        'collection': collection,
        'model': model,
        'question': question,
        'prompt': prompt,
        'answer': answer,
        'answer_with_context': answer_with_context
    }]

if __name__ == '__main__':
    # initialize lists
    collection_list = ['char_splitter_1024_o128_replicate', 'char_splitter_1024_o128_spacy', 'article_regex_splitter_spacy', 'article_regex_splitter_replicate', 'semantic_splitter_spacy', 'semantic_splitter_replicate']
    models_list = ['mistralai/mixtral-8x7b-instruct-v0.1'] ## more models to add
    prompt_list = [prompt_template_role_prompting, prompt_template_zero_shot, prompt_template_one_shot] ## to extend
        
    # chroma client    
    chroma_client = chromadb.PersistentClient(path="../resources/chromadb")
    
    # source of questions and answers
    source_qa = '../resources/TestFragen/'
        
    df_output = pd.DataFrame(columns=['collection', 'model', 'question', 'prompt', 'answer', 'answer_with_context'])
    count = 0
    index = 1
    for collection in collection_list:
        for model in models_list:
            for filename in os.listdir(source_qa):
                if filename.endswith(".json"):
                    df = pd.read_json(source_qa + filename)
                    for index, row in df.iterrows():
                        question = row['question']
                        answer = row['answer']
                        for prompt_template in prompt_list:
                            result = process_question(collection, model, question, answer, prompt_template, source_qa)
                            
                            df_1 = pd.DataFrame(result)
                            df_output = pd.concat([df_output, df_1], ignore_index=True)
                            
                            if count % 10 == 0:
                                df_output.to_json(f'../resources/Testset/output_{collection}{index}.json')
                                index += 1
                            
                            count+=1
                            # df_ouput = df_output.append(result, ignore_index=True)
        
        df_output.to_json(f'../resources/Testset/output_{collection}.json')
