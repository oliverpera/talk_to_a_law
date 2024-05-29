import pandas as pd
import json

from transformers import AutoModel, AutoTokenizer
from transformers import BertTokenizer, BertModel
from bert_score import BERTScorer
import numpy as np
import torch
from transformers import BertTokenizer, BertModel
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
# Pfad zur JSON-Datei
json_file_path = r'/root/talk_to_a_law/src/resources/Testset/final_test_df.json'

# JSON-Datei laden
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Konvertiere JSON-Daten in einen DataFrame 
df = pd.DataFrame(data)

# DataFrame anzeigen
print(df.columns)







# Load the tokenizer and model
tokenizer = BertTokenizer.from_pretrained('google-bert/bert-base-german-cased')
model = BertModel.from_pretrained('google-bert/bert-base-german-cased')

# Function to get embeddings for a text
def get_embeddings(texte):
    inputs = tokenizer(texte, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    # Use the last hidden state
    last_hidden_state = outputs.last_hidden_state
    # Mean pooling to get sentence embeddings
    sentence_embeddings = last_hidden_state.mean(dim=1)
    return sentence_embeddings


def getCosins(df):
    similaritylist = []
    for index, text in df.iterrows():
        print()
        sentence1 = "Das ist ein Beispielsatz."
        sentence2 = "Hier ist ein anderer Satz."

        # Get embeddings for each sentence
        
        #print(Satz1)
        print(text.answer)
        Satz1 = text.answer.replace('\n', ' ')
        Satz123 = str(Satz1)
        embedding1 = get_embeddings(sentence1)
        Satz231 = text.answer_with_context.replace('\n', ' ')
        Satz231 = str(Satz2)
        embedding2 = get_embeddings(sentence2)

        # Convert to numpy arrays
        embedding1_np = embedding1.numpy()
        embedding2_np = embedding2.numpy()

        # Calculate cosine similarity
        similarity = cosine_similarity(embedding1_np, embedding2_np)

        print("Cosine Similarity:", similarity[0][0])
        similaritylist.append(similarity[0][0])
        print(np.mean(similaritylist))


splitter =['semantic_splitter_spacy','semantic_splitter_replicate','char_splitter_1024_o128_spacy','char_splitter_1024_o128_replicate','article_regex_splitter_spacy','article_regex_splitter_replicate']
model = ['mistralai/mixtral-8x7b-instruct-v0.1','meta/meta-llama-3-70b-instruct',]
prompt= ['Als','Beantworte']

getCosins(df)


for split in splitter:
    for mod in model:
        for promp in prompt:

            mask = df['prompt'].str.split().str[0] == promp
            df_filtered = df[mask]
            mask = df_filtered['model'] == mod
            df_filtered1 = df_filtered[mask]
            mask = df_filtered1['collection'] == split
            df_filtered2 = df_filtered1[mask]
            #print(df_filtered2)
            #print(df_filtered2.iat[1,4])
            tester = str(df_filtered2.iat[1,4])
            print(tester)
            print(get_embeddings(tester))
            getCosins(df_filtered2)