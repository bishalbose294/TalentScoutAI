from src.utils.database import DBConnector
import configparser, uuid, os
from datetime import datetime, timedelta
import dateutil.relativedelta as relativedelta

config = configparser.ConfigParser()
config.read("configs/config.cfg")
db_config = config["DATABASE"]
schema = db_config["SCHEMA"]
fileTable = db_config['FILETABLE']
upload_capacity = int(db_config['UPLOADCAPACITY'])
expiration_days = int(db_config['EXPIRATIONDAYS'])

class FileManagement:

    def __init__(self):
        self.db = DBConnector()
        pass

    def __checkIfFileExists(self, fileId):
        sql = f"""select fileId from {schema}.{fileTable} where fileId='{fileId}' """
        result = self.db.select(sql)
        if result is None:
            return False
        elif len(result[0])==0:
            return False
        return True
        pass

    def uploadFile(self, fileName, email, fileType):
        fileId = str(uuid.uuid4())
        timestamp = datetime.now()
        sql = f"""insert into {schema}.{fileTable} values ('{fileId}','{email}','{fileName}','{fileType}','{timestamp}')"""
        result = self.db.insert(sql)
        return fileId
        pass


    def deleteFiles(self, email, folderPath, fileIdList):
        
        search_condition = ""
        for i in range(len(fileIdList)):
            if i == len(fileIdList)-1:
                search_condition += f"'{fileIdList[i]}'"
            else:
                search_condition += f"'{fileIdList[i]}' , "

        sql = f""" select fileType, fileName from {schema}.{fileTable} where email = '{email}' and fileId IN ({search_condition}) """
        results = self.db.select(sql)

        for result in results:
            filePath = os.path.join(folderPath, result[0], result[1])
            if os.path.exists(filePath):
                os.remove(filePath)
            else:
                print(f"{filePath} file does not exist")

        sql = f""" delete from {schema}.{fileTable} where fileId IN ({search_condition}) """
        self.db.delete(sql)
        return "Successfully Deleted"
        pass

    def downloadFile(self, email, folderPath, fileId):

        if not self.__checkIfFileExists(fileId):
            return "No Such File"

        sql = f""" select fileType, fileName from {schema}.{fileTable} where fileId = '{fileId}' and email = '{email}' """
        result = self.db.select(sql)
        return os.path.join(folderPath, result[0][0], result[0][1])
        pass

    def getFileMetaList(self, email):
        sql = f""" select fileId, fileName, fileType from {schema}.{fileTable} where email = '{email}' """
        results = self.db.select(sql)
        fileDict = dict()
        for result in results:
            fileId = result[0]
            filename = result[1]
            fileType = result[2]

            fileDict[fileId] = {"filename": filename, "fileType": fileType}
        return fileDict
        pass


    def ifFileUploadable(self, folder):
        if len(os.listdir(folder)) >= upload_capacity:
            return False
        return True
        pass

    def emptyFolder(self, folders):

        criticalTime = (datetime.now() - relativedelta.relativedelta(days=expiration_days)).timestamp()

        print(criticalTime)

        for folder in folders:
         if not folder[2]:
            os.chmod(folder[0], 0o777)
            try:
               os.rmdir(folder[0])
            except Exception as ex:
               print(ex)
               pass
        
         else:
             for file in folder[2]:
                filePath = os.path.join(folder[0],file)
                item_time = os.stat(filePath).st_ctime
                if item_time < criticalTime:
                    os.remove(filePath)

        d = datetime.now() - relativedelta.relativedelta(days=expiration_days)
        sql = f""" delete from {schema}.{fileTable} where timestamp < '{d}' """
        self.db.delete(sql)
        print(f"Files deleted")
        pass

    pass