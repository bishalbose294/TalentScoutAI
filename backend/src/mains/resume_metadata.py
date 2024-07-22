import re, os
from pdfminer.high_level import extract_text
import spacy
from spacy.matcher import Matcher
from src.utils.commonutils import CommonUtils
from src.mains.resume_analyzer import ResumeAnalyzer

class ResumeMetaData():

    def __init__(self) -> None:
        self.utils = CommonUtils()
        self.analyzer = ResumeAnalyzer()
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
    
    def extractMetaData(self, resumeFolder):

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

    pass


if __name__ == '__main__':

    resumeFolder = "D:/Study Material/Projects/HR Assist/Code/test_data/RESUMES"

    metadata = ResumeMetaData()
    info = metadata.extractMetaData(resumeFolder)

    print(info)

    pass