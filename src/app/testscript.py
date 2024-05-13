
import pandas as pd
import chromadb
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

# def test_script():
#     pass



def set_prompt(collection, question, prompt_templ):
    query_result = collection.query(
        # query_embeddings=[], # embedded question / part of question # HERE: PREFORMULATE ANSWER, EMBED ANSWER, RETRIEVE REAL KNOWLEDGE ?!? # needs to be the same dimension as embedded vectors in db
        query_texts=[question], # ALTERNATIVE THAN QUERYING WITH EMBEDDINGS -> CHROMA WILL AUTOMATICALLY EMBED USING EMBEDDING FUNCTION OF COLLECTION
        n_results=4, # number of docs to retrieve
        # where={"metadata_field": "is_equal_to_this"}, # filter metadata
        # where_document={"$contains": "search_string"}, # filter for hard words / regexes etc.
        # include=["documents"], # specify which data to return (embeddings is excluded by default)
    )
    
    documents = query_result['documents']            
    context = '\n'.join([item.replace('\xad\n', '') for document in documents for item in document])
    prompt = prompt_templ.format(query=question, context=context)
    return prompt
    
def get_collection(name):
    # case:
        #### EMBEDDING FUNCTION HINZUFÜGEN
    return chroma_client.get_collection(name=name, embedding_function=SpacyEmbeddingsFunction())


# if __name__ == '__main__':
    
#     # initialize lists
#     collection_list = ['char_splitter_128_o0']
#     models_list = ['meta/llama-2-7b-chat', 'mistralai/mixtral-8x7b-instruct-v0.1']
#     prompt_list = [prompt_template_role_prompting, prompt_template_zero_shot, prompt_template_one_shot]
    
#     # chroma client    
#     chroma_client = chromadb.PersistentClient(path="../resources/chromadb")


#     # source of questions and answers
#     source_qa = '../resources/TestFragen/'
#     df = pd.read_json(source_qa + 'CELEX_02013L0036-20220101_DE_TXT.json')
    
    
    
    
#     df_output = pd.DataFrame(columns=['collection', 'model', 'question', 'prompt' 'answer', 'answer_with_context'])

    
    
#     print(df.head())
#     print(df.iloc[2]['question'])
#     print(df.iloc[2]['answer'])
    
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
    collection_list = ['char_splitter_128_o0']
    models_list = ['meta/llama-2-7b-chat', 'mistralai/mixtral-8x7b-instruct-v0.1']
    prompt_list = [prompt_template_role_prompting, prompt_template_zero_shot, prompt_template_one_shot]
        
    # chroma client    
    chroma_client = chromadb.PersistentClient(path="../resources/chromadb")
    # source of questions and answers
    source_qa = '../resources/TestFragen/'
    # df = pd.read_json(source_qa + 'CELEX_02013L0036-20220101_DE_TXT.json')
        
    df_output = pd.DataFrame(columns=['collection', 'model', 'question', 'prompt', 'answer', 'answer_with_context'])
    count = 0
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
                            
                            if count == 5:
                                df_output.to_json(f'../resources/Testset/output_{collection}.json')
                                break
                            count+=1
                            # df_ouput = df_output.append(result, ignore_index=True)
        
        df_output.to_json(f'../resources/Testset/output_{collection}.json')
