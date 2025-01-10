import sqlite3
import configparser

config = configparser.ConfigParser()
config.read("TalentScoutAI/configs/config.cfg")
db_config = config["DATABASE"]
db_file = db_config['DBNAME']

class DBConnector:

    def __init__(self) -> None:
        table_list = []
        self.createConnection()
        
        table_list.append(f""" CREATE TABLE if not exists {db_config["LOGINTABLE"]} (
                    email VARCHAR(255) PRIMARY KEY,
                    password VARCHAR(255) NOT NULL
                ); """)

        table_list.append(f""" CREATE TABLE if not exists {db_config["CREDITTABLE"]} (
                    email VARCHAR(255) PRIMARY KEY,
                    credits FLOAT NOT NULL
                ); """)
        
        for table in table_list:
            try:
                self.cursor.execute(table)
            except Exception as ex:
                print(ex)

        self.closeConection()
        pass

    def createConnection(self,):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        pass

    def closeConection(self,):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        pass

    def checkIfTableExists(self, table_name):
        sql = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        pass

    def insert(self, sql):
        self.createConnection()
        insertedData = self.cursor.execute(sql)
        self.closeConection()
        return insertedData
        pass

    def delete(self, sql):
        self.createConnection()
        deletedData = self.cursor.execute(sql)
        self.closeConection()
        return deletedData
        pass

    def select(self, sql):
        self.createConnection()
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.closeConection()
        return result
        pass

    def update(self, sql):
        self.createConnection()
        updatedData = self.cursor.execute(sql)
        self.closeConection()
        return updatedData
    pass
