import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

## unfortunately the original data is not available, so I created a dummy data to visualize the results
data = {
    "Rank": range(1, 29),
    "prompt": [
        "zero_shot", "zero_shot", "role", "zero_shot", "zero_shot", "role", "zero_shot",
        "zero_shot", "role", "role", "role", "role", "zero_shot", "zero_shot", "zero_shot",
        "zero_shot", "zero_shot", "role", "role", "role", "zero_shot", "role", "role", "role",
        "role", "zero_shot", "role", "zero_shot"
        ],
    "model": [
        "llama3", "llama3", "llama3", "llama3", "llama3", "llama3", "llama3", "llama3", "llama3",
        "llama3", "llama3", "llama3", "mixtral", "mixtral", "mixtral", "mixtral", "mixtral", "mixtral",
        "mixtral", "mixtral", "mixtral", "mixtral", "mixtral", "mixtral", "llama3", "llama3", "mixtral",
        "mixtral" 
        ],
    "splitter": [
        "Char", "Article Regex", "Char",
        "Char", "Semantic", "Article Regex", "Article Regex",
        "Semantic", "Semantic", "Semantic", "Char",
        "Article Regex", "Char", "Char", "Article Regex",
        "Article Regex", "Semantic", "Char", "Char",
        "Article Regex", "Semantic", "Article Regex", "Semantic", "Semantic",
        "benchmark", "benchmark", "benchmark", "benchmark"
    ],
    "embedding_model_vectordb": [
        "replicate_all_mpnetbase_v2", "replicate_all_mpnetbase_v2", "replicate_all_mpnetbase_v2", 
        "spacy_de_core_news_lg", "replicate_all_mpnetbase_v2", "replicate_all_mpnetbase_v2",
        "spacy_de_core_news_lg", "spacy_de_core_news_lg", "replicate_all_mpnetbase_v2", "spacy_de_core_news_lg",
        "spacy_de_core_news_lg", "spacy_de_core_news_lg", "replicate_all_mpnetbase_v2", "spacy_de_core_news_lg",
        "replicate_all_mpnetbase_v2", "spacy_de_core_news_lg", "replicate_all_mpnetbase_v2", "replicate_all_mpnetbase_v2",
        "spacy_de_core_news_lg", "spacy_de_core_news_lg", "spacy_de_core_news_lg", "replicate_all_mpnetbase_v2",
        "replicate_all_mpnetbase_v2", "spacy_de_core_news_lg", "benchmark", "benchmark", "benchmark", "benchmark"
    ],
    "cosine_similarity": [
        0.94990003, 0.9454018, 0.9439096, 0.9427309, 0.9422775, 0.9421219, 0.941865, 0.94040877,
        0.9372982, 0.9362696, 0.93593365, 0.93495566, 0.9074232, 0.90356374, 0.9010663, 0.8996756,
        0.8986304, 0.8978463, 0.8970864, 0.8961337, 0.89509326, 0.89194274, 0.89175516, 0.891711,
        0.8871897, 0.875515, 0.86416614, 0.8537382
    ]
}

df = pd.DataFrame(data)
df.head()

plt.figure(figsize=(15, 10))

# 1. Cosine Similarity Distribution by Prompt Type
plt.subplot(2, 2, 1)
sns.boxplot(x="prompt", y="cosine_similarity", data=df)
plt.title('Cosine Similarity Distribution by Prompt Type')
plt.ylabel('Cosine Similarity')

# 2. Average Cosine Similarity by Model
plt.subplot(2, 2, 2)
sns.barplot(x="model", y="cosine_similarity", data=df, ci=None)
plt.title('Average Cosine Similarity by Model')
plt.xlabel('Model')
plt.ylabel('Average Cosine Similarity')

# 3. Cosine Similarity by Splitter
plt.subplot(2, 2, 3)
sns.boxplot(x="splitter", y="cosine_similarity", data=df)
plt.title('Cosine Similarity by Splitter')
plt.ylabel('Cosine Similarity')
plt.xticks(rotation=90)


# 3. Cosine Similarity by Splitter
plt.subplot(2, 2, 4)
sns.boxplot(x="embedding_model_vectordb", y="cosine_similarity", data=df)
plt.title('Cosine Similarity by Embedding Model')
plt.ylabel('Cosine Similarity')
plt.xticks(rotation=90)

plt.tight_layout()
plt.show()


