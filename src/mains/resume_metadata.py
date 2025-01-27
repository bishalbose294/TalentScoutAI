import re, os, configparser
import simplejson as json
from pdfminer.high_level import extract_text
import spacy
from spacy.matcher import Matcher
from src.utils.commonutils import CommonUtils
from src.mains.resume_analyzer import ResumeAnalyzer
from src.utils.database import DBConnector
from datetime import datetime


config = configparser.ConfigParser()
config.read("configs/config.cfg")
db_config = config["DATABASE"]
schema = db_config["SCHEMA"]
fileTable = db_config['FILETABLE']
keywordTable = db_config['KEYWORDTABLE']

class ResumeMetaData():

    def __init__(self) -> None:
        self.utils = CommonUtils()
        self.analyzer = ResumeAnalyzer()
        self.db = DBConnector()
        pass


    def extract_text_from_pdf(self, pdf_path):
        return extract_text(pdf_path)


    def extract_contact_number_from_resume(self, text):
        contact_number = None
        # Use regex pattern to find a potential contact number
        pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
        tmp = re.findall(pattern,text)
        r1 = '[^0-9]+'
        contact_number_list = []
        for con in tmp:
            contact_number_list.append(re.sub(r1, "", con)[-10:])

        contact_number = ", ".join(contact_number_list)

        return contact_number


    def extract_email_from_resume(self, text):
        email = None
        # Use regex pattern to find a potential email address
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        email = ", ".join(re.findall(pattern,text))
        return email
    

    def extract_education_from_resume(self, text):
        education = []

        # Use regex pattern to find education information
        pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.\w+|\bBachelor(?:'s)?|\bMaster(?:'s)?|\bPh\.D)\s(?:\w+\s)*\w+"
        matches = re.findall(pattern, text)
        for match in matches:
            education.append(match.strip())

        return education


    def extract_name(self, resume_text):
        nlp = spacy.load('en_core_web_lg')
        matcher = Matcher(nlp.vocab)

        # Define name patterns
        patterns = [
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name and Last name
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name, Middle name, and Last name
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]  # First name, Middle name, Middle name, and Last name
            # Add more patterns as needed
        ]

        for pattern in patterns:
            matcher.add('NAME', patterns=[pattern])

        doc = nlp(resume_text)
        matches = matcher(doc)

        for match_id, start, end in matches:
            span = doc[start:end]
            return span.text

        return None
    
    def extract_links_extended(self, text):
        links = []
        pattern = r'\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b'
        links = re.findall(pattern, text)
        for link in links:
            if "/" not in link:
                links.remove(link)
        return links
    

    def extract_keywords(self, text):
        return self.analyzer.extractKeywords(text)
    
    def extractMetaData(self, basePath, email, fileId):

        sql = f""" select fileName, fileType from {schema}.{fileTable} where email = '{email}' and fileId = '{fileId}' """

        results = self.db.select(sql)

        fileName = results[0][0]
        fileType = results[0][1]

        resumePath = os.path.join(basePath,email,fileType,fileName)


        resume_info = dict()
        text = self.extract_text_from_pdf(resumePath)

        name = self.extract_name(text)
        if name:
            resume_info["Name"] = name
        else:
            resume_info["Name"] = ""


        contact_number = self.extract_contact_number_from_resume(text)
        if contact_number:
            resume_info["Contact Number"] = contact_number
        else:
            resume_info["Contact Number"] = ""


        email = self.extract_email_from_resume(text)
        if email:
            resume_info["Email"] = email
        else:
            print("Email not found")


        extracted_education = self.extract_education_from_resume(text)
        if extracted_education:
            resume_info["Education"] = extracted_education
        else:
            resume_info["Education"] = ""


        extracted_links = self.extract_links_extended(text)
        if extracted_education:
            resume_info["Links"] = extracted_links
        else:
            resume_info["Links"] = ""


        extracted_keywords = self.extract_keywords(text)
        if extracted_keywords:
            resume_info["Skills"] = extracted_keywords
        else:
            resume_info["Skills"] = ""
        
        timestamp = datetime.now()

        resume_info = json.dumps(resume_info).replace("'","\"")

        sql = f""" INSERT into {schema}.{keywordTable} values ('{fileId}','{resume_info}','{timestamp}') """

        self.db.insert(sql)
        
        return resume_info
    
    def extractMetaData_fromFolder(self, resumeFolder):

        resume_list = os.listdir(resumeFolder)
        resume_info = dict()

        for resume in resume_list:
            print(resume)
            meta_data = dict()
            resume_path = os.path.join(resumeFolder, resume)
            text = self.extract_text_from_pdf(resume_path)


            name = self.extract_name(text)
            if name:
                meta_data["Name"] = name
            else:
                meta_data["Name"] = ""


            contact_number = self.extract_contact_number_from_resume(text)
            if contact_number:
                meta_data["Contact Number"] = contact_number
            else:
                meta_data["Contact Number"] = ""


            email = self.extract_email_from_resume(text)
            if email:
                meta_data["Email"] = email
            else:
                print("Email not found")


            extracted_education = self.extract_education_from_resume(text)
            if extracted_education:
                meta_data["Education"] = extracted_education
            else:
                meta_data["Education"] = ""


            extracted_links = self.extract_links_extended(text)
            if extracted_education:
                meta_data["Links"] = extracted_links
            else:
                meta_data["Links"] = ""


            extracted_keywords = self.extract_keywords(text)
            if extracted_keywords:
                meta_data["Skills"] = extracted_keywords
            else:
                meta_data["Skills"] = ""
            
            resume_info[resume] = meta_data
        
        return resume_info
    
    def getExtractedKeywords(self, fileId):
        sql = f""" select extracted_info from {schema}.{keywordTable} where fileId = '{fileId}' """
        results = self.db.select(sql)
        return {"extracted_info": json.loads(results[0][0])}
        pass

    pass
