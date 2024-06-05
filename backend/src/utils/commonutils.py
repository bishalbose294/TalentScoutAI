import os
import json
import re


class CommonUtils:

    def __init__(self) -> None:
        pass

    def loadStropwords(self,):
        with open(os.path.join("src", "configs", "stopwords.txt"), "r") as g:
            stopwords = g.read().splitlines()
        return stopwords

    def loadAbbreviations(self,):
        with open(os.path.join("src", "configs", "abbr.json"), "r") as json_file:
            data = json.load(json_file)
        return data
    
    def has_numbers(self, inputString):
        return bool(re.search(r'\d', inputString))

    pass



if __name__ == "__main__":

    cu = CommonUtils()
    print(type(cu.loadAbbreviations()))
    print(cu.loadAbbreviations())


    pass