import psycopg2
import configparser

config = configparser.ConfigParser()
config.read("TalentScoutAI/backend/src/configs/config.cfg")
db_config = config["DATABASE"]

class DBConnector:

    def __init__(self) -> None:
        pass

    def createConnection(self,):
        self.connection = psycopg2.connect(database=db_config["DBNAME"], user=db_config["USER"], password=db_config["PASSWORD"], host=db_config["HOST"], port=db_config["PORT"])
        self.schema = db_config["SCHEMA"]
        self.cursor = self.connection.cursor()
        pass

    def closeConection(self,):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        pass

    def insert(self, sql, valueList):
        self.createConnection()
        insertedData = self.cursor.executemany(sql, valueList)
        self.closeConection()
        return insertedData
        pass

    def delete(self, sql, values):
        self.createConnection()
        deletedData = self.cursor.execute(sql, values)
        self.closeConection()
        return deletedData
        pass

    def select(self, sql, values):
        self.createConnection()
        self.cursor.execute(sql, values)
        result = self.cursor.fetchall()
        self.closeConection()
        return result
        pass

    def update(self, sql, values):
        self.createConnection()
        updatedData = self.cursor.execute(sql, values)
        self.closeConection()
        return updatedData

    pass
