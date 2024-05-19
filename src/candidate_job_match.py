import os
from chunking import Chunk
from compare_metrics import CompareMetrics


class MatchJobCandidate:

    def __init__(self) -> None:
        self.compareMetrics = CompareMetrics()
        pass


    def compare(self, sent1, sent2):
        return self.compareMetrics.calculate_similarity(sent1, sent2)
        pass

    def match(self, jdFile, resumeFile):
        chunkJd = Chunk(jdFile)
        chunkResume = Chunk(resumeFile)

        jdChunkList = chunkJd.chunk()
        resumeChunkList = chunkResume.chunk()

        for jdchunk in jdChunkList:
            for resumechunk in resumeChunkList:
                print(self.compare(jdchunk,resumechunk))
        pass

    def run(self, jodDescFolder, resumeFolder):
        jd_list = os.listdir(jodDescFolder)
        resume_list = os.listdir(resumeFolder)

        for jd in jd_list:
            for resume in resume_list:
                jdFile = os.path.join(jodDescFolder, jd)
                resumeFile = os.path.join(resumeFolder, resume)
                # print(jd)
                # print(resume)
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