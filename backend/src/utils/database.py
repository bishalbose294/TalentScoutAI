import mysql.connector
import configparser

config = configparser.ConfigParser()
config.read("TalentScoutAI/backend/src/configs/config.cfg")
db_config = config["DB"]

class DBConnector:

    def __init__(self) -> None:

        self.mydb = mysql.connector.connect(
                    host=db_config["HOST"],
                    user=db_config["USER"],
                    password=db_config["PASSWORD"],
                    database=db_config["DATABASE"],
                )
        
        pass

    def createConection(self,):
        self.mycursor = self.mydb.cursor()
        pass

    def commitData(self,):
        self.mydb.commit()
        pass

    def closeConection(self,):
        self.mycursor.close()
        self.mydb.close()
        pass

    def insertData(self, query, values):
        self.createConection()
        self.mycursor.execute(query, values)
        self.commitData()
        self.closeConection()
        return self.mycursor.rowcount
        pass

    def deleteData(self, query):
        self.createConection()
        self.mycursor.execute(query)
        self.commitData()
        self.closeConection()
        return self.mycursor.rowcount
        pass

    def getData(self, query):
        self.createConection()
        self.mycursor.execute(query)
        result = self.mycursor.fetchone()[0]
        self.closeConection()
        return result
        pass

    def updateData(self, query):
        self.createConection()
        self.mycursor.execute(query)
        self.commitData()
        self.closeConection()
        return self.mycursor.rowcount

    pass
