from src.utils.database import DBConnector
import configparser, uuid, os
from datetime import datetime


config = configparser.ConfigParser()
config.read("configs/config.cfg")
db_config = config["DATABASE"]
schema = db_config["SCHEMA"]
table = db_config['FILETABLE']

class FileManagement:

    def __init__(self):
        self.db = DBConnector()
        pass

    def uploadFile(self, fileName, email, fileType):
        fileId = str(uuid.uuid4())
        timestamp = datetime.now()
        sql = f"""insert into {schema}.{table} values ('{fileId}','{email}','{fileName}','{fileType}','{timestamp}')"""
        result = self.db.insert(sql)
        return "Success"
        pass


    def deleteFiles(self, email, folderPath, fileIdList):
        
        search_condition = ""
        for i in range(len(fileIdList)):
            if i == len(fileIdList)-1:
                search_condition += f"'{fileIdList[i]}'"
            else:
                search_condition += f"'{fileIdList[i]}' , "

        sql = f""" select fileType, fileName from {schema}.{table} where email = '{email}' and fileId IN ({search_condition}) """
        results = self.db.select(sql)

        for result in results:
            filePath = os.path.join(folderPath, result[0], result[1])
            if os.path.exists(filePath):
                os.remove(filePath)
            else:
                print(f"{filePath} file does not exist")

        sql = f""" delete from {schema}.{table} where fileId IN ({search_condition}) """
        self.db.delete(sql)
        return "Successfully Deleted"
        pass

    def downloadFile(self, email, folderPath, fileId):
        sql = f""" select fileType, fileName from {schema}.{table} where fileId = '{fileId}' and email = '{email}' """
        result = self.db.select(sql)
        return os.path.join(folderPath, result[0][0], result[0][1])

        pass

    def getFileMetaList(self, email):
        sql = f""" select fileId, fileName, fileType from {schema}.{table} where email = '{email}' """
        results = self.db.select(sql)
        fileDict = dict()
        for result in results:
            fileId = result[0]
            filename = result[1]
            fileType = result[2]
            fileDict[fileId] = {"filename": filename, "fileType": fileType}
        return fileDict
        pass

    pass