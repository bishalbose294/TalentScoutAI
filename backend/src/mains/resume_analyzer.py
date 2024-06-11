from src.text.text_cleaning import TextCleaner
from src.text.embeddings import SentEmbeddings
from src.utils.compare_metrics import CompareMetrics
import configparser, os
from src.text.keywords import KeyphraseExtractionPipeline
from src.text.chunking import Chunk
from transformers import pipeline


config = configparser.ConfigParser()
config.read("src/configs/config.cfg")
analyzer_config = config["ANALYZER"]

topKey = float(analyzer_config["TOP_KEYWORDS"])
maxGram = float(analyzer_config["MAX_KEYWORDS_SIZE"])
matchThreshold = float(analyzer_config["KEYWORD_MATCH_THRESHOLD"])
resume_summarizer = analyzer_config["RESUME_SUMMARIZER"]
maxlength = int(analyzer_config["RESUME_MAXLENGTH"])
minlength = int(analyzer_config["RESUME_MINLENGTH"])

class ResumeAnalyzer:

    def __init__(self) -> None:

        self.keywordExtractor = KeyphraseExtractionPipeline()
        self.cleaning = TextCleaner()
        self.embeddings = SentEmbeddings()
        self.compare = CompareMetrics()
        self.chunk = Chunk(chunksize=1000, overlap=100)
        self.summarizer = pipeline("summarization", model=resume_summarizer)
        
        pass


    def extractKeywords(self, text):
        keywords = self.keywordExtractor(text)
        keylist = []
        for kw in keywords:
            keylist.append(self.cleaning.clean_text(kw))
        
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
    
    # def __summarize(self, text):
    #     print("Summarizer Called")
    #     return self.summarizer(text, max_length=maxlength, min_length=minlength, do_sample=False)[0]["summary_text"]
    #     pass

    def __summarizeBatch(self, textBatch):
        return self.summarizer(textBatch, max_length=maxlength, min_length=minlength, do_sample=False)
        pass

    # def resumeSummarizer(self, resumeFile):
    #     resumeChunk_list = self.chunk.chunk(resumeFile)
    #     summarize = ""
    #     summareized_list = self.__summarize(resumeChunk_list)
    #     for summary in summareized_list:
    #         summarize += " "+summary["summary_text"]
    #     return summarize
    #     pass

    def resumeBatchSummarizer(self, resumeFolder):
        resume_list = os.listdir(resumeFolder)

        resumeSummarize = dict()

        for resumeFile in resume_list:
            file = os.path.join(resumeFolder, resumeFile)
            resumeChunk_list = self.chunk.chunk(file)
            response = self.__summarizeBatch(resumeChunk_list)
            print(response)
            summarize = ""
            for summary in response:
                summarize += " "+str(summary['summary_text'])
            resumeSummarize[resumeFile] = summarize

        return resumeSummarize
        pass
    
    pass
