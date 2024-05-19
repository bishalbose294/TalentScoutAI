
from sentence_transformers import util
from embeddings import SentEmbeddings
from text_cleaning import TextCleaner

class CompareMetrics:

    def __init__(self) -> None:
        self.sentEmbedding = SentEmbeddings()
        self.textCleaner = TextCleaner()
        pass
    
    def dot_score(self, sent1, sent2):
        emb1 = self.sentEmbedding.computeEmbedding(sent1)
        emb2 = self.sentEmbedding.computeEmbedding(sent2)
        return round(util.dot_score(emb1, emb2).numpy()[0][0].tolist(),2)

    def cos_sim(self, sent1, sent2):
        emb1 = self.sentEmbedding.computeEmbedding(sent1)
        emb2 = self.sentEmbedding.computeEmbedding(sent2)
        return round(util.cos_sim(emb1, emb2).numpy()[0][0].tolist(),2)

    def calculate_similarity(self, sent1, sent2):
        metrics = dict()
        cleaned_sent1 = self.textCleaner.clean_text(sent1)
        cleaned_sent2 = self.textCleaner.clean_text(sent2)
        metrics['dot_score'] = self.dot_score(cleaned_sent1, cleaned_sent2)
        metrics['cos_sim'] = self.cos_sim(cleaned_sent1, cleaned_sent2)

        ## sending only cos_sim as both are same
        return metrics['cos_sim']

    pass
