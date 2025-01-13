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

    def uploadFile(self, fileName, email):
        fileId = str(uuid.uuid4())
        timestamp = datetime.now()
        sql = f"""insert into {schema}.{table} values ('{fileId}','{email}','{fileName}','{timestamp}')"""
        result = self.db.insert(sql)
        return "Success"
        pass


    def deleteFiles(self, fileIdList, filePathList):
        
        for filePath in filePathList:
            if os.path.exists(filePath):
                os.remove(filePath)
            else:
                return "The file does not exist"
            pass
        
        search_condition = ""
        for i in range(len(fileIdList)):
            if i == len(fileIdList)-1:
                search_condition += f"'{fileIdList[i]}'"
            else:
                search_condition += f"'{fileIdList[i]}' , "

        sql = f""" delete from {schema}.{table} where fileId IN in {search_condition})"""
        result = self.db.delete(sql)
        return "Success"
        pass

    def downloadFile(self, fileId):
        sql = f""" select fileName from {schema}.{table} where fileId = {fileId}"""
        result = self.db.select(sql)
        return result
        pass

    def getFileMetaList(self, email):
        sql = f""" select * from {schema}.{table} where email = {email}"""
        result = self.db.select(sql)
        return result
        pass

    pass