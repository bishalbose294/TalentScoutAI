import os, json, re
from datetime import datetime
from dateutil import relativedelta

class CommonUtils:

    def __init__(self) -> None:
        pass

    def loadStropwords(self,):
        with open(os.path.join("TalentScoutAI", "configs", "stopwords.txt"), "r") as g:
            stopwords = g.read().splitlines()
        return stopwords

    def loadAbbreviations(self,):
        with open(os.path.join("TalentScoutAI", "configs", "abbr.json"), "r") as json_file:
            data = json.load(json_file)
        return data
    
    def has_numbers(self, inputString):
        return bool(re.search(r'\d', inputString))


    def get_number_of_months_from_dates(date1, date2):
        if date2.lower() == 'present':
            date2 = datetime.now().strftime('%b %Y')
        try:
            if len(date1.split()[0]) > 3:
                date1 = date1.split()
                date1 = date1[0][:3] + ' ' + date1[1]
            if len(date2.split()[0]) > 3:
                date2 = date2.split()
                date2 = date2[0][:3] + ' ' + date2[1]
        except IndexError:
            return 0
        try:
            date1 = datetime.strptime(str(date1), '%b %Y')
            date2 = datetime.strptime(str(date2), '%b %Y')
            months_of_experience = relativedelta.relativedelta(date2, date1)
            months_of_experience = (months_of_experience.years
                                    * 12 + months_of_experience.months)
        except ValueError:
            return 0
        return months_of_experience

    pass




if __name__ == "__main__":

    cu = CommonUtils()
    print(type(cu.loadAbbreviations()))
    print(cu.loadAbbreviations())


    pass