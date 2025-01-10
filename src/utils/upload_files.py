from TalentScoutAI.src.utils.database import DBConnector


class UploadFiles:

    def __init__(self):
        
        self.db = DBConnector()

        pass


    def uploadFile(self, filePath, email):
        pass

    def deleteFile(self, uniqueId):
        pass

    def downloadFile(self, uniqueId):
        pass

    def getFileMetaList(self, email):
        pass

    pass