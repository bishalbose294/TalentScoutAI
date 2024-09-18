from TalentScoutAI.backend.src.utils.database import DBConnector


class LoginClass:

    def __init__(self,) -> None:
        self.dbconnect = DBConnector()
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
