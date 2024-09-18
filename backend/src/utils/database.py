from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import configparser

config = configparser.ConfigParser()
config.read("TalentScoutAI/backend/src/configs/config.cfg")
db_config = config["DB"]

class DBConnector:

    def __init__(self) -> None:
        pass

    def createConnection(self,):
        self.pyMongoClient = MongoClient(db_config["CONNECTIONSTRING"], server_api=ServerApi("1"))
        self.db = self.pyMongoClient[db_config["DATABASE"]]
        self.collection = self.db[db_config["LOGINCOLLECTION"]]
        pass

    def closeConection(self,):
        self.pyMongoClient.close()
        pass

    def insertOne(self, data):
        self.createConnection()
        insertedData = self.collection.insert_one(data)
        self.closeConection()
        return insertedData.inserted_id
        pass

    def insertMany(self, data):
        self.createConnection()
        insertedData = self.collection.insert_many(data)
        self.closeConection()
        return insertedData.inserted_id
        pass

    def deleteOne(self, data):
        self.createConnection()
        deletedData = self.collection.delete_one(data)
        self.closeConection()
        return deletedData.deleted_count
        pass

    def deleteMany(self, data):
        self.createConnection()
        deletedData = self.collection.delete_many(data)
        self.closeConection()
        return deletedData.deleted_count
        pass

    def getOne(self, data):
        self.createConnection()
        result = self.collection.find_one(data)
        self.closeConection()
        return result
        pass

    def getMany(self, data):
        self.createConnection()
        result = self.collection.find(data)
        self.closeConection()
        return result
        pass

    def updateOne(self, search, update):
        self.createConnection()
        updatedData = self.collection.update_one(search, update)
        self.closeConection()
        return updatedData.modified_count

    def updateMany(self, search, update):
        self.createConnection()
        updatedData = self.collection.update_many(search, update)
        self.closeConection()
        return updatedData.modified_count

    pass
