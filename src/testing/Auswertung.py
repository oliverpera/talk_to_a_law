import pandas as pd
import json
from transformers import AutoModel, AutoTokenizer
from transformers import BertModel, BertTokenizer
import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity
import os


print(os.getcwd())
#Hier Pfad anpassen
json_file_path = r'/root/talk_to_a_law/src/resources/Testset/final_test_df.json'


with open(json_file_path, 'r') as file:
    data = json.load(file)


df1 = pd.DataFrame(data)

NewData = {
    'Art': [' '],
    'Cosin': [0]
    }
finaldf = pd.DataFrame(NewData)

tokenizer = BertTokenizer.from_pretrained('google-bert/bert-base-german-cased')
model = BertModel.from_pretrained('google-bert/bert-base-german-cased')

def getCosins(df):
    similaritylist = []
    for index, answer_chatbot in df.iterrows():
        text = copy.deepcopy(answer_chatbot.answer)
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        last_hidden_state = outputs.last_hidden_state
        embedding1 = last_hidden_state.mean(dim=1)

        text = copy.deepcopy(answer_chatbot.answer_with_context)
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        last_hidden_state = outputs.last_hidden_state
        embedding2 = last_hidden_state.mean(dim=1)

        embedding1_np = embedding1.numpy()
        embedding2_np = embedding2.numpy()

        similarity = cosine_similarity(embedding1_np, embedding2_np)
        similaritylist.append(similarity[0][0])
    
    print(np.mean(similaritylist)) 
    return np.mean(similaritylist)


splitter = ['semantic_splitter_spacy','semantic_splitter_replicate','char_splitter_1024_o128_spacy','char_splitter_1024_o128_replicate','article_regex_splitter_spacy','article_regex_splitter_replicate']
modele = ['mistralai/mixtral-8x7b-instruct-v0.1','meta/meta-llama-3-70b-instruct',]
prompt = ['Als','Beantworte']


for split in splitter:
    for mod in modele:
        for promp in prompt:

            mask = df1['prompt'].str.split().str[0] == promp
            df_filtered = df1[mask]
            mask = df_filtered['model'] == mod
            df_filtered1 = df_filtered[mask]
            mask = df_filtered1['collection'] == split
            df_filtered2 = df_filtered1[mask]
            Cosin = getCosins(df_filtered2)
            result = str(split) + " " + str(mod) + " " + str(promp)
            NextAnswer = {
            'Art': [result],
            'Cosin': [Cosin]
                }

            finaldf.loc[len(finaldf)] = NextAnswer
            print(finaldf)
            print(result)
            
            

finaldf.to_excel ("Cosin.xlsx", index=False)          
