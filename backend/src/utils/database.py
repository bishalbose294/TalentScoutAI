import sqlite3
import configparser

config = configparser.ConfigParser()
config.read("TalentScoutAI/backend/src/configs/config.cfg")
db_config = config["DATABASE"]
db_file = db_config['DBNAME']

class DBConnector:

    def __init__(self) -> None:
        try:
            self.createConnection()

            # Creating table
            table = f""" CREATE TABLE {db_config["LOGINTABLE"]} (
                        email VARCHAR(255) PRIMARY KEY,
                        password VARCHAR(255) NOT NULL
                    ); """
            
            self.cursor.execute(table)

            # Creating table
            table = f""" CREATE TABLE {db_config["CREDITTABLE"]} (
                        email VARCHAR(255) PRIMARY KEY,
                        credits FLOAT NOT NULL
                    ); """
            
            self.cursor.execute(table)

            self.closeConection()
        except Exception as ex:
            print(ex)
            pass
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
