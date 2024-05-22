import yake
from src.text.text_cleaning import TextCleaner
from src.text.embeddings import SentEmbeddings
from src.utils.compare_metrics import CompareMetrics
import configparser

config = configparser.ConfigParser()
config.read("src/configs/config.cfg")
analyzer_config = config["ANALYZER"]

topKey = float(analyzer_config["TOP_KEYWORDS"])
maxGram = float(analyzer_config["MAX_KEYWORDS_SIZE"])
matchThreshold = float(analyzer_config["KEYWORD_MATCH_THRESHOLD"])


class ResumeAnalyzer:

    def __init__(self) -> None:

        self.custom_kw_extractor = yake.KeywordExtractor(lan="en", n=3, dedupLim=0.9, dedupFunc='seqm', 
                                                         windowsSize=5, top=20, features=None)
        
        self.cleaning = TextCleaner()
        self.embeddings = SentEmbeddings()
        self.compare = CompareMetrics()
        
        pass


    def extractKeywords(self, text):
        keywords = self.custom_kw_extractor.extract_keywords(text)
        keylist = []
        for kw in keywords:
            keylist.append(self.cleaning.clean_text(kw[0]))
        
        return keylist
        pass


    def keywordsPartialMatch(self, jdKeywords, resumeKeywords):

        jdKeywords = sorted(list(set(jdKeywords)))
        resumeKeywords = sorted(list(set(resumeKeywords)))

        jdKeywords_embed = self.embeddings.computeEmbeddingList(jdKeywords)
        resumeKeywords_embed = self.embeddings.computeEmbeddingList(resumeKeywords)

        match_jd_res_key = dict()

        for i in range(len(jdKeywords)):
            resKeys = []
            for j in range(len(resumeKeywords)):
                
                metric = self.compare.cos_sim(jdKeywords_embed[i], resumeKeywords_embed[j])
                if metric > matchThreshold:
                    resKeys.append(resumeKeywords[j])
            
            if resKeys:
                match_jd_res_key[jdKeywords[i]] = resKeys

        return match_jd_res_key
        pass
    
    pass