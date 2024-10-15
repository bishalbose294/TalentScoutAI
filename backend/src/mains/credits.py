from TalentScoutAI.backend.src.utils.database import DBConnector
import configparser

config = configparser.ConfigParser()
config.read("TalentScoutAI/backend/src/configs/config.cfg")
db_config = config["DATABASE"]
schema = db_config["SCHEMA"]
table = db_config["LOGINTABLE"]

class Credits:

    def __init__(self) -> None:
        pass

    def add_credits(self, credits):
        pass

    def substract_credits(self, credits):
        pass

    pass