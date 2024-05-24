import os
from src.text.chunking import Chunk
from src.utils.compare_metrics import CompareMetrics
from src.mains.resume_analyzer import ResumeAnalyzer
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
        pass


    def compare(self, sent1, sent2):
        return self.compareMetrics.calculate_similarity(sent1, sent2)
        pass

    def match(self, jdFile, resumeFile):

        metric = []
        jdChunkList = self.chunk.chunk(jdFile)
        resumeChunkList = self.chunk.chunk(resumeFile)

        for jdchunk in jdChunkList:
            for resumechunk in resumeChunkList:
                value = self.compare(jdchunk,resumechunk)
                if value > 0.5:
                    metric.append(1)
        
        return sum(metric)
        
        pass

    def keywordsMatch(self, jdFile, resumeFile):

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
                metric = self.match(jdFile, resumeFile)
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
                resume_dict[resume] = self.keywordsMatch(jdFile, resumeFile)
                
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