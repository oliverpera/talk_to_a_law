import pandas as pd
import json

from transformers import AutoModel, AutoTokenizer
from transformers import BertTokenizer, BertModel
from bert_score import BERTScorer
import numpy as np
# Pfad zur JSON-Datei
json_file_path = r'/root/talk_to_a_law/src/resources/Testset/final_test_df.json'

# JSON-Datei laden
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Konvertiere JSON-Daten in einen DataFrame 
df = pd.DataFrame(data)

# DataFrame anzeigen
print(df.columns)


tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-base-german-cased")
model = AutoModel.from_pretrained("dbmdz/bert-base-german-cased")


from transformers import BertTokenizer, BertModel
from bert_score import BERTScorer
# Example texts
reference = ["This is a reference text example."]
candidate = ["This is a candidate text example."]

df_filtered = df[df['model'] != 'mistralai/mixtral-8x7b-instruct-v0.1']


# BERTScore calculation
scorer = BERTScorer(model_type='bert-base-uncased')
P, R, F1 = scorer.score(df_filtered['answer'].values, df_filtered['answer_with_context'].values)
print(f"BERTScore Precision: {P.mean():.4f}, Recall: {R.mean():.4f}, F1: {F1.mean():.4f}")