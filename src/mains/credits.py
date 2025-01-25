from src.utils.database import DBConnector
import configparser

config = configparser.ConfigParser()
config.read("configs/config.cfg")
db_config = config["DATABASE"]
schema = db_config["SCHEMA"]
creditTable = db_config["CREDITTABLE"]

class Credits:

    def __init__(self) -> None:
        self.db = DBConnector()
        pass

    def get_credits(self, email):
        sql = f""" select credits from {schema}.{creditTable} WHERE email = '{email}' """
        result = self.db.select(sql)
        return {"balance_credits": str(int(result[0][0]))}
        pass

    def add_credits(self, email, credits):

        balance_credits = int(self.get_credits(email)["balance_credits"])
        
        sql = f""" UPDATE {schema}.{creditTable} SET credits = {int(balance_credits+credits)} WHERE email = '{email}' """
        self.db.update(sql)

        return {"msg": f"{credits} added successfully", "balance_credits": str(int(balance_credits+credits))}
        pass

    def substract_credits(self, email, credits):
        
        balance_credits = int(self.get_credits(email)["balance_credits"])
        
        sql = f""" UPDATE {schema}.{creditTable} SET credits = {int(balance_credits-credits)} WHERE email = '{email}' """
        self.db.update(sql)

        return {"msg": f"{credits} removed successfully", "balance_credits": str(int(balance_credits-credits))}
        pass

    def check_sufficient_credit(self, email, creditsToBeUsed):
        balance_credits = int(self.get_credits(email)["balance_credits"])
        if balance_credits < creditsToBeUsed:
            return False
        return True
        pass

    pass