
import re, os
from pdfminer.high_level import extract_text
import spacy
from spacy.matcher import Matcher


class ResumeMetaData():

    def __init__(self) -> None:
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
    
    def extractMetaData(self, resumeFolder):

        resume_list = os.listdir(resumeFolder)
        resume_info = dict()

        for resume in resume_list:
            print(resume)
            meta_data = dict()
            resume_path = os.path.join(resumeFolder, resume)
            text = resumemetadata.extract_text_from_pdf(resume_path)

            name = resumemetadata.extract_name(text)
            if name:
                meta_data["Name"] = name
            else:
                meta_data["Name"] = ""


            contact_number = resumemetadata.extract_contact_number_from_resume(text)
            if contact_number:
                meta_data["Contact Number"] = contact_number
            else:
                meta_data["Contact Number"] = ""


            email = resumemetadata.extract_email_from_resume(text)
            if email:
                meta_data["Email"] = email
            else:
                print("Email not found")


            extracted_education = resumemetadata.extract_education_from_resume(text)
            if extracted_education:
                meta_data["Education"] = extracted_education
            else:
                meta_data["Education"] = ""
                    
            resume_info[resume] = meta_data
        
        return resume_info

    pass


if __name__ == '__main__':

    resumeFolder = "D:/Study Material/Projects/HR Assist/Code/test_data/RESUMES"

    resumemetadata = ResumeMetaData()
    info = resumemetadata.extractMetaData(resumeFolder)

    print(info)

    pass