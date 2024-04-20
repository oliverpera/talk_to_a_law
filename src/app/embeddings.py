import spacy
from chromadb import Documents, EmbeddingFunction, Embeddings

class SpacyEmbeddingsFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        nlp = spacy.load("de_core_news_sm") # md , lg , trf (bert-base-german-cased)
        embeddings = [nlp(document).vector.tolist() for document in input]
        return embeddings
spacy_ef = SpacyEmbeddingsFunction()