from TalentScoutAI.backend.src.utils.database import DBConnector
import configparser

config = configparser.ConfigParser()
config.read("TalentScoutAI/backend/src/configs/config.cfg")
db_config = config["DATABASE"]
schema = db_config["SCHEMA"]
table = db_config["LOGINTABLE"]


class LoginClass:

    def __init__(self,) -> None:
        self.dbconnect = DBConnector()
        pass

    def userLogin(self, email, password):
        sql = f"""select * from {schema}.{table} where "emailId"=%s and "password"=%s """
        values = (email, password,)
        result = self.dbconnect.select(sql, values)
        if result:
            return "Success"
        else:
            return "Failure"
        pass

    def userRegister(self, email, password):
        sql = f"""insert into {schema}.{table} values (%s,%s)"""
        values = [
                (email,password),
        ]
        result = self.dbconnect.insert(sql, values)
        return "Success"
        pass

    def userLogout(self, email,):
        pass

    pass
