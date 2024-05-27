import os
from src.text.chunking import Chunk
from src.utils.compare_metrics import CompareMetrics
from src.mains.resume_analyzer import ResumeAnalyzer
from src.text.embeddings import SentEmbeddings
import configparser

config = configparser.ConfigParser()
config.read("src/configs/config.cfg")
candidate_config = config["CANDIDATE"]

pointsThreshold = int(candidate_config["RESUME_MATCH_POINT_THRESHOLD"])

class MatchJobCandidate:

    def __init__(self) -> None:
        self.compareMetrics = CompareMetrics()
        self.analyzer = ResumeAnalyzer()
        self.chunk = Chunk()
        self.embedding = SentEmbeddings()
        pass

    def __match(self, jdFile, resumeFile):

        metric = []
        jdChunkList = self.chunk.chunk(jdFile)
        resumeChunkList = self.chunk.chunk(resumeFile)

        jdchunkEmbeddings = self.embedding.computeEmbeddingList(jdChunkList)
        jdresumeEmbeddings = self.embedding.computeEmbeddingList(resumeChunkList)

        for jdchunkembed in jdchunkEmbeddings:
            for resumechunkembed in jdresumeEmbeddings:
                value = self.compareMetrics.cos_sim(jdchunkembed,resumechunkembed)
                if value > 0.5:
                    metric.append(1)
        
        return sum(metric)
        
        pass

    def __keywordsMatch(self, jdFile, resumeFile):

        jdtext = self.chunk.getTextFromPdf(jdFile)
        resumeText = self.chunk.getTextFromPdf(resumeFile)

        keywordsJD = self.analyzer.extractKeywords(jdtext)

        keywordsRES = self.analyzer.extractKeywords(resumeText)

        return self.analyzer.keywordsPartialMatch(keywordsJD, keywordsRES)
        pass

    def generatePointers(self, jodDescFolder, resumeFolder):
        jd_list = os.listdir(jodDescFolder)
        resume_list = os.listdir(resumeFolder)

        jd_dict = dict()

        for jd in jd_list:

            resume_dict = dict()

            for resume in resume_list:
                jdFile = os.path.join(jodDescFolder, jd)
                resumeFile = os.path.join(resumeFolder, resume)
                metric = self.__match(jdFile, resumeFile)
                resume_dict[resume] = metric
            
            jd_dict[jd] = {k: v for k, v in sorted(resume_dict.items(), key=lambda item: item[1], reverse=True)}
        
        return jd_dict
        pass

    def extractJDResumeKeywords(self, jodDescFolder, resumeFolder):
        jd_list = os.listdir(jodDescFolder)
        resume_list = os.listdir(resumeFolder)

        jd_dict = dict()

        for jd in jd_list:

            resume_dict = dict()

            for resume in resume_list:
                jdFile = os.path.join(jodDescFolder, jd)
                resumeFile = os.path.join(resumeFolder, resume)
                resume_dict[resume] = self.__keywordsMatch(jdFile, resumeFile)
                
            jd_dict[jd] = resume_dict
        
        return jd_dict
        pass

    pass

if __name__ == "__main__":
    match = MatchJobCandidate()
    jodDescFolder = "D:/Study Material/HR Assist/Code/Talent-Scout-AI/test_data/JDS"
    resumeFolder = "D:/Study Material/HR Assist/Code/Talent-Scout-AI/test_data/RESUMES"
    match.run(jodDescFolder, resumeFolder)
    pass