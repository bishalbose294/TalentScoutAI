import os
from src.text.chunking import Chunk
from src.utils.compare_metrics import CompareMetrics
from src.mains.resume_analyzer import ResumeAnalyzer
from src.text.embeddings import SentEmbeddings
from src.utils.commonutils import CommonUtils
import configparser

config = configparser.ConfigParser()
config.read("src/configs/config.cfg")
candidate_config = config["CANDIDATE"]

pointsThreshold = int(candidate_config["RESUME_MATCH_POINT_THRESHOLD"])
sectionMatchThreshold = int(candidate_config["SECTION_MATCH_POINT_THRESHOLD"])

class MatchJobCandidate:

    def __init__(self) -> None:
        self.compareMetrics = CompareMetrics()
        self.analyzer = ResumeAnalyzer()
        self.chunk = Chunk()
        self.embedding = SentEmbeddings()
        self.utility = CommonUtils()
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
                if value > sectionMatchThreshold:
                    metric.append(1)
        
        return sum(metric)
        
        pass

    def __keywordsMatch(self, jdFile, resumeFile):

        jdtext_list = self.chunk.chunk(jdFile)
        resumeText_list = self.chunk.chunk(resumeFile)
        
        keywordsJD=[]
        for jdtext in jdtext_list:
            keywordsJD.extend(self.analyzer.extractKeywords(jdtext))

        keywordsJD = sorted(list(set(keywordsJD)))
    
        keywordsRES = []
        for resumeText in resumeText_list:
            keywordsRES.extend(self.analyzer.extractKeywords(resumeText))
        
        keywordsRES = sorted(list(set(keywordsRES)))
        resumeKey = []
        for keyword in keywordsRES:
            if not self.utility.has_numbers(keyword):
                resumeKey.append(keyword)

        return self.analyzer.keywordsPartialMatch(keywordsJD, keywordsRES), resumeKey
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
                resume_dict[resume], resume_dict[resume]["resume_keywords"]  = self.__keywordsMatch(jdFile, resumeFile)
                
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