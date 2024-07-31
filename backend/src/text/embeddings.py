from sentence_transformers import SentenceTransformer
from TalentScoutAI.backend.src.text.text_cleaning import TextCleaner
import configparser

config = configparser.ConfigParser()
config.read("src/configs/config.cfg")
embed_config = config["EMBEDDINGS"]


class SentEmbeddings():
    
    def __init__(self) -> None:
        self.model = SentenceTransformer(embed_config['SENTENCE_TRANSFORMER'], trust_remote_code=True, device='cuda')
        pass

    def computeEmbedding(self, sentence):
        cleaner = TextCleaner()
        clean_sent = cleaner.clean_text(sentence)
        return self.model.encode(clean_sent)
        pass

    def computeEmbeddingList(self, sentenceList):
        cleaner = TextCleaner()
        cleaned_sentList = []
        for i in range(len(sentenceList)):
           cleaned_sentList.append(cleaner.clean_text(sentenceList[i]))
        return self.model.encode(cleaned_sentList)
        pass
    
    pass


if __name__ == "__main__":
    embed = SentEmbeddings()
    test_sent = """This isn't a panda,,,, you are wrong this is a well versed bear    ..
                                        which you'll never understand!!!!!!!!!!!!!!!!"""
    embedding = embed.computeEmbedding(test_sent)
    print(embedding)
    pass