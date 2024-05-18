from sentence_transformers import SentenceTransformer
import re
import configparser

config = configparser.ConfigParser()
config.read("config.cfg")
embed_config = config["EMBEDDINGS"]

class SentEmbeddings():
    
    def __init__(self) -> None:
        self.model = SentenceTransformer(embed_config['SENTENCE_TRANSFORMER'])
        pass

    # remove all the unnecessay characters from the text
    def __removeSpecialChars(self, phrase):
        phrase = phrase.replace('\\r', ' ')
        phrase = phrase.replace('\\"', ' ')
        phrase = phrase.replace('\\n', ' ')
        phrase = re.sub('[^A-Za-z0-9]+', ' ', phrase)
        phrase = re.sub(' +',' ',phrase)
        phrase = phrase.strip().lower()
        return phrase

    def __clean_text(self, phrase):
        # specific
        phrase = re.sub(r"won't", "will not", phrase)
        phrase = re.sub(r"can\'t", "can not", phrase)
        # general
        phrase = re.sub(r"n\'t", " not", phrase)
        phrase = re.sub(r"\'re", " are", phrase)
        phrase = re.sub(r"\'s", " is", phrase)
        phrase = re.sub(r"\'d", " would", phrase)
        phrase = re.sub(r"\'ll", " will", phrase)
        phrase = re.sub(r"\'t", " not", phrase)
        phrase = re.sub(r"\'ve", " have", phrase)
        phrase = re.sub(r"\'m", " am", phrase)
        phrase = re.sub(r"nan" , '' , phrase)
        phrase = self.__removeSpecialChars(phrase)
        return phrase

    def computeEmbedding(self, sentence):
        clean_sent = self.__clean_text(sentence)
        return self.model.encode(clean_sent)
        pass

    pass


if __name__ == "__main__":
    embed = SentEmbeddings()
    test_sent = """This isn't a panda,,,, you are wrong this is a well versed bear    ..
                                        which you'll never understand!!!!!!!!!!!!!!!!"""
    embedding = embed.computeEmbedding(test_sent)
    print(embedding)
    pass