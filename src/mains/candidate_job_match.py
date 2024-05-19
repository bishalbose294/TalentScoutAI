import os
from text.chunking import Chunk
from utils.compare_metrics import CompareMetrics


class MatchJobCandidate:

    def __init__(self) -> None:
        self.compareMetrics = CompareMetrics()
        pass


    def compare(self, sent1, sent2):
        return self.compareMetrics.calculate_similarity(sent1, sent2)
        pass

    def match(self, jdFile, resumeFile):

        metric = []

        chunkJd = Chunk()
        chunkResume = Chunk()

        jdChunkList = chunkJd.chunk(jdFile)
        resumeChunkList = chunkResume.chunk(resumeFile)

        print("Jd Chunk - ",len(jdChunkList))
        print("Resume Chunk - ",len(resumeChunkList))

        for jdchunk in jdChunkList:
            for resumechunk in resumeChunkList:
                value = self.compare(jdchunk,resumechunk)
                if value > 0.5:
                    metric.append(value)
        
        print(metric)
        
        pass

    def keywordsMatch(self,):
        pass

    def run(self, jodDescFolder, resumeFolder):
        jd_list = os.listdir(jodDescFolder)
        resume_list = os.listdir(resumeFolder)

        for jd in jd_list:
            for resume in resume_list:
                jdFile = os.path.join(jodDescFolder, jd)
                resumeFile = os.path.join(resumeFolder, resume)
                print("\n\n")
                print(jd)
                print(resume)
                self.match(jdFile, resumeFile)
            break
        pass

    pass

if __name__ == "__main__":
    match = MatchJobCandidate()
    jodDescFolder = "D:/Study Material/HR Assist/Code/Talent-Scout-AI/test_data/JDS"
    resumeFolder = "D:/Study Material/HR Assist/Code/Talent-Scout-AI/test_data/RESUMES"
    match.run(jodDescFolder, resumeFolder)
    pass