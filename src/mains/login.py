from TalentScoutAI.src.utils.database import DBConnector
import configparser

config = configparser.ConfigParser()
config.read("TalentScoutAI/configs/config.cfg")
db_config = config["DATABASE"]
schema = db_config["SCHEMA"]
table = db_config["LOGINTABLE"]


class LoginClass:

    def __init__(self,) -> None:
        self.dbconnect = DBConnector()
        pass

    def userLogin(self, email, password):
        sql = f"""select * from {schema}.{table} where email='{email}' and password='{password}' """
        result = self.dbconnect.select(sql)
        if result:
            return "Success"
        else:
            return "Failure"
        pass

    def userRegister(self, email, password):
        sql = f"""insert into {schema}.{table} values ('{email}','{password}')"""
        result = self.dbconnect.insert(sql)
        return "Success"
        pass

    def userLogout(self, email,):
        pass

    pass
