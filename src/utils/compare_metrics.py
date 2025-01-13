
from sentence_transformers import util
from src.text.embeddings import SentEmbeddings
from src.text.text_cleaning import TextCleaner
from typing import List
from qdrant_client import QdrantClient
import configparser

config = configparser.ConfigParser()
config.read("configs/config.cfg")
embed_config = config["EMBEDDINGS"]

class CompareMetrics:

    def __init__(self) -> None:
        self.sentEmbedding = SentEmbeddings()
        self.textCleaner = TextCleaner()
        pass
    
    def dot_score(self, emb1, emb2):
        return round(util.dot_score(emb1, emb2).numpy()[0][0].tolist(),2)

    def cos_sim(self, emb1, emb2):
        return round(util.cos_sim(emb1, emb2).numpy()[0][0].tolist(),2)

    def calculate_similarity(self, sent1, sent2):
        metrics = dict()
        cleaned_sent1 = self.textCleaner.clean_text(sent1)
        cleaned_sent2 = self.textCleaner.clean_text(sent2)
        
        emb1 = self.sentEmbedding.computeEmbedding(cleaned_sent1)
        emb2 = self.sentEmbedding.computeEmbedding(cleaned_sent2)
        metrics['dot_score'] = self.dot_score(emb1, emb2)
        metrics['cos_sim'] = self.cos_sim(emb1, emb2)

        ## sending only cos_sim as both are same
        return metrics['cos_sim']
    
    
    def get_score(self, resume_string, job_description_string):

        documents: List[str] = [resume_string]
        client = QdrantClient(":memory:")
        client.set_model(embed_config['SCORING_EMBED']) 

        client.add(
            collection_name="demo_collection",
            documents=documents,
        )

        search_result = client.query(
            collection_name="demo_collection", query_text=job_description_string
        )
        
        return search_result

    pass
