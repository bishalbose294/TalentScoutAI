from TalentScoutAI.backend.src.utils.database import DBConnector
import configparser

config = configparser.ConfigParser()
config.read("TalentScoutAI/backend/src/configs/config.cfg")
db_config = config["DB"]


class LoginClass:

    def __init__(self,) -> None:
        collectioName = db_config["LOGINCOLLECTION"]
        self.dbconnect = DBConnector(collectioName)
        pass

    def userLogin(self, email, password):
        data = {"email": email, "password": password}
        result = self.dbconnect.getOne(data)
        if result:
            return "Success"
        else:
            return "Failure"
        pass

    def userRegister(self, email, password):
        data = {"email": email, "password": password}
        result = self.dbconnect.insertOne(data)
        if result:
            return "Success"
        else:
            return "Failure"
        pass

    def userLogout(self,):
        pass

    pass
