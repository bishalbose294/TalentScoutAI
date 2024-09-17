from TalentScoutAI.backend.src.utils.database import DBConnector


class LoginClass:

    def __init__(self,) -> None:
        self.dbconnect = DBConnector()
        pass

    def userLogin(self, email, password):
        query = f"select count(*) from user_creds where email_id='{email}' and password='{password}'"
        result = self.dbconnect.getData(query)
        if result:
            return "Success"
        else:
            return "Failure"
        pass

    def userRegister(self, email, password):
        query = f"insert into user_creds (email_id, password) VALUES (%s, %s)"
        values = (email, password)
        result = self.dbconnect.insertData(query, values)
        if result:
            return "Success"
        else:
            return "Failure"
        pass

    def userLogout(self,):
        pass

    pass
