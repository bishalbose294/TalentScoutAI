import os
from src.text.chunking import Chunk
from src.utils.compare_metrics import CompareMetrics
from src.mains.resume_analyzer import ResumeAnalyzer
from src.text.embeddings import SentEmbeddings
from src.utils.commonutils import CommonUtils
from src.text.text_cleaning import TextCleaner
from src.utils.database import DBConnector
import configparser
from datetime import datetime


config = configparser.ConfigParser()
config.read("configs/config.cfg")
candidate_config = config["CANDIDATE"]

db_config = config["DATABASE"]
schema = db_config["SCHEMA"]
fileTable = db_config["FILETABLE"]
jd_resume_match_table = db_config["JDRESUMEMATCHTABLE"]

pointsThreshold = int(candidate_config["RESUME_MATCH_POINT_THRESHOLD"])
sectionMatchThreshold = float(candidate_config["SECTION_MATCH_POINT_THRESHOLD"])

class MatchJobCandidate:

    def __init__(self) -> None:
        self.compareMetrics = CompareMetrics()
        self.chunk = Chunk()
        self.utility = CommonUtils()
        self.cleaner = TextCleaner()
        self.db = DBConnector()
        pass

    def __match(self, jdFile, resumeFile):

        self.embedding = SentEmbeddings()

        metric = 0
        jdChunkList = self.chunk.chunk(jdFile)
        resumeChunkList = self.chunk.chunk(resumeFile)

        jdchunkEmbeddings = self.embedding.computeEmbeddingList(jdChunkList)
        jdresumeEmbeddings = self.embedding.computeEmbeddingList(resumeChunkList)

        total_compare = len(jdchunkEmbeddings) * len(jdresumeEmbeddings)

        for i in range(len(jdchunkEmbeddings)):
            for j in range(len(jdresumeEmbeddings)):
                metric += self.compareMetrics.cos_sim(jdchunkEmbeddings[i],jdresumeEmbeddings[j])
        
        return round((metric*100)/total_compare,2)
        
        pass

    def __keywordsMatch(self, jdFile, resumeFile):

        self.analyzer = ResumeAnalyzer()

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
    

    def generatePointer(self, email, basePath, jdFileId, resumeFileId):
        
        sql = f""" select fileName, fileType from {schema}.{fileTable} where email = '{email}' and fileId = '{jdFileId}' or fileId = '{resumeFileId}' """

        results = self.db.select(sql)

        resumePath = None
        jdPath = None
        for result in results:
            fileType = result[1]
            fileName = result[0]
            if fileType == "resumes":
                resumePath = os.path.join(basePath,email,fileType,fileName)
            elif fileType == "jds":
                jdPath = os.path.join(basePath,email,fileType,fileName)
        
        metric = self.__match(jdPath, resumePath)
        
        return metric
        pass

    def generateBatchPointers(self, jodDescFolder, resumeFolder):
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

    def extractJDResumeKeyword(self, email, basePath, jdFileId, resumeFileId):
        
        sql = f""" select fileName, fileType from {schema}.{fileTable} where email = '{email}' and fileId = '{jdFileId}' or fileId = '{resumeFileId}' """

        results = self.db.select(sql)

        resumePath = None
        jdPath = None
        for result in results:
            fileType = result[1]
            fileName = result[0]
            if fileType == "resumes":
                resumePath = os.path.join(basePath,email,fileType,fileName)
            elif fileType == "jds":
                jdPath = os.path.join(basePath,email,fileType,fileName)

        
        jd_resume_keywords_match, resume_keywords  = self.__keywordsMatch(jdPath, resumePath)
        
        return jd_resume_keywords_match, resume_keywords
        pass

    def matchJdResume(self, email, basePath, jdFileId, resumeFileId):
        metric = self.generatePointer(email, basePath, jdFileId, resumeFileId)
        jd_resume_keywords_match, resume_keywords = self.extractJDResumeKeyword(email, basePath, jdFileId, resumeFileId)

        timestamp = datetime.now()

        jd_resume_keywords_match_db = str(jd_resume_keywords_match).replace("\'","\"")
        resume_keywords_db = str(resume_keywords).replace("\'","\"")

        sql = f""" insert into {schema}.{jd_resume_match_table} values ('{jdFileId}','{resumeFileId}','{str(metric)}','{jd_resume_keywords_match_db}','{resume_keywords_db}','{timestamp}') """

        self.db.insert(sql)

        return metric, jd_resume_keywords_match, resume_keywords
        pass


    def extractBatchJDResumeKeywords(self, jodDescFolder, resumeFolder):
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

    def getJDResumeScore(self, jodDescFolder, resumeFolder):
        jd_list = os.listdir(jodDescFolder)
        resume_list = os.listdir(resumeFolder)

        jd_dict = dict()
        for jd in jd_list:
            jdText = self.cleaner.clean_text(self.chunk.getTextFromPdf(os.path.join(jodDescFolder, jd)))
            resume_dict = dict()
            for resume in resume_list:
                resumeText = self.cleaner.clean_text(self.chunk.getTextFromPdf(os.path.join(resumeFolder, resume)))
                results = self.compareMetrics.get_score(resumeText, jdText)
                resume_dict[resume] = results[0].score
            jd_dict[jd] = resume_dict
        
        return jd_dict

    pass