import psycopg2
import configparser

config = configparser.ConfigParser()
config.read("TalentScoutAI/backend/src/configs/config.cfg")
db_config = config["DB"]

class DBConnector:

    def __init__(self) -> None:
        pass

    def createConnection(self,):
        self.connection = psycopg2.connect(database=db_config["DBNAME"], user=db_config["USER"], password=db_config["PASSWORD"], host=db_config["HOST"], port=db_config["PORT"])
        self.schema = db_config["SCHEMA"]
        self.cursor = self.connection.cursor()
        pass

    def closeConection(self,):
        self.cursor.close()
        self.connection.close()
        pass

    def insertOne(self, sql, values):
        self.createConnection()
        insertedData = self.cursor.execute(sql, (values,))
        self.closeConection()
        return insertedData
        pass

    def insertMany(self, sql, valueList):
        self.createConnection()
        insertedData = self.cursor.execute(sql, valueList)
        self.closeConection()
        return insertedData
        pass

    def deleteOne(self, sql, values):
        self.createConnection()
        deletedData = self.cursor.execute(sql, (values,))
        self.closeConection()
        return deletedData
        pass

    def deleteMany(self, sql, valueList):
        self.createConnection()
        deletedData = self.cursor.execute(sql, valueList)
        self.closeConection()
        return deletedData
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

    def updateOne(self, sql, updateValue, searchValue):
        self.createConnection()
        updatedData = self.cursor.execute(sql, (updateValue, searchValue))
        self.closeConection()
        return updatedData

    def updateMany(self, search, update):
        self.createConnection()
        updatedData = self.collection.update_many(search, update)
        self.closeConection()
        return updatedData.modified_count

    pass
