import pandas as pd
import json
from transformers import AutoModel, AutoTokenizer
from transformers import BertModel, BertTokenizer
import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity
import os
import copy
import math


print(os.getcwd())
#Hier Pfad anpassen
json_file_path = r'/root/talk_to_a_law/src/resources/Testset/baseline_test_df.json'


with open(json_file_path, 'r') as file:
    data = json.load(file)


df1 = pd.DataFrame(data)

print(df1)

json_file_path = r'/root/talk_to_a_law/src/resources/Testset/final_test_df.json'


with open(json_file_path, 'r') as file:
    data = json.load(file)


df2 = pd.DataFrame(data)


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
        if type(answer_chatbot.realAnswer) == str:
            inputs = tokenizer(answer_chatbot.realAnswer, return_tensors='pt', truncation=True, padding=True)
            with torch.no_grad():
                outputs = model(**inputs)
            last_hidden_state = outputs.last_hidden_state
            embedding1 = last_hidden_state.mean(dim=1)
        else: 
            continue

        inputs = tokenizer(answer_chatbot.answer, return_tensors='pt', truncation=True, padding=True)
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

mask = df2['prompt'].str.split().str[0] == 'Als'
df_filtered = df2[mask]
mask = df_filtered['model'] == 'mistralai/mixtral-8x7b-instruct-v0.1'
df_filtered1 = df_filtered[mask]
mask = df_filtered['collection'] == 'article_regex_splitter_replicate'
df_alt = df_filtered[mask]



modele = ['mistralai/mixtral-8x7b-instruct-v0.1','meta/meta-llama-3-70b-instruct',]
prompt = ['role','zero_shot']



for mod in modele:
    for promp in prompt:

        mask = df1['prompt_template'].str.split().str[0] == promp
        df_filtered = df1[mask]
        mask = df_filtered['model'] == mod
        df_filtered1 = df_filtered[mask]
        df_filtered1['realAnswer'] = df_alt['answer']
        print(df_filtered1['realAnswer'])
        print(df_filtered1['realAnswer'].values)
        Cosin = getCosins(df_filtered1)
        result = str(mod) + " " + str(promp)
        NextAnswer = {
        'Art': [result],
        'Cosin': [Cosin]
            }

        finaldf.loc[len(finaldf)] = NextAnswer
        print(finaldf)
        print(result)
            
            

finaldf.to_excel ("Cosin.xlsx", index=False)          
