from flask import Flask, redirect, url_for, render_template, request, jsonify, send_file
from flask_cors import CORS
import simplejson as json
import os, traceback
from src.mains.candidate_job_match import MatchJobCandidate
from src.mains.resume_analyzer import ResumeAnalyzer
from src.mains.resume_metadata import ResumeMetaData
from src.utils.file_management import FileManagement
from src.mains.credits import Credits
from src.mains.login import LoginClass
from flask_ngrok import run_with_ngrok
from pyngrok import ngrok
from gevent.pywsgi import WSGIServer
import warnings
import configparser

config = configparser.ConfigParser()
config.read("configs/config.cfg")
api_config = config["API"]

credit_config = config['CREDITS']

calculate_scores_charges = int(credit_config['CALCULATE_SCORES'])
summarize_resume_charges = int(credit_config['SUMMARIZE_RESUME'])
extract_resume_metadata_charges = int(credit_config['EXTRACT_RESUME_METADATA'])

warnings.filterwarnings("ignore")

os.environ['CUDA_LAUNCH_BLOCKING']="1"
os.environ['TORCH_USE_CUDA_DSA'] = "1"


app = Flask(__name__)
CORS(app=app)


cwd = os.getcwd()
app.config["ALLOWED_EXTENSIONS"] = [".pdf"]
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024 # 25 MB
app.config["UPLOAD_FOLDER"] = os.path.join(cwd, "data")

methods = ['POST']

def cleanFolder():
   try:
      fileMgmt = FileManagement()
      folders = list(os.walk(app.config["UPLOAD_FOLDER"]))[1:]
      fileMgmt.emptyFolder(folders)
   except:
      print(traceback.format_exc())
   pass

@app.route("/")
def home():
   return "Server up & running"

def calculate_scores():
   try:

      email = request.get_json()['email']
      jdFileId = request.get_json()['jdFileId']
      resumeFileId = request.get_json()['resumeFileId']

      cred = Credits()
      if not cred.check_sufficient_credit(email, calculate_scores_charges):
         return jsonify({"msg": "Insufficient Credit Balance"})
      
      match = MatchJobCandidate()
      metric, jd_resume_keywords_match, resume_keywords = match.matchJdResume(email, app.config["UPLOAD_FOLDER"], jdFileId, resumeFileId)

      subtract = calculate_scores_charges
      if "msg" in response.keys():
         subtract = 0
      credit_response = cred.substract_credits(email, subtract)

      response = {"match_point": metric, "resume_keywords": resume_keywords, "jd_resume_keywords_match": jd_resume_keywords_match}

      return jsonify({"response": response, "credits": credit_response})
   
   except Exception as ex:
      print("Exception: ",ex.with_traceback)
      print(traceback.format_exc())
      return jsonify({"error": str(ex), "traceback": traceback.format_exc()})
   finally:
      cleanFolder()
      pass
   
app.add_url_rule("/calculate_scores", 'calculate_scores', calculate_scores, methods=methods)

def get_calculated_scores():
   email = request.get_json()['email']
   jdFileId = request.get_json()['jdFileId']
   resumeFileId = request.get_json()['resumeFileId']

   match = MatchJobCandidate()
   metric, jd_resume_keywords_match, resume_keywords = match.getCalculatedScores(email, jdFileId, resumeFileId)

   return jsonify({"match_point": json.loads(metric), "resume_keywords": json.loads(resume_keywords), "jd_resume_keywords_match": json.loads(jd_resume_keywords_match)})
   pass

app.add_url_rule("/get_calculated_scores", 'get_calculated_scores', get_calculated_scores, methods=methods)

def summarize_resume():
   try:

      email = request.get_json()['email']
      fileId = request.get_json()['fileId']

      cred = Credits()
      if not cred.check_sufficient_credit(email, summarize_resume_charges):
         return jsonify({"msg": "Insufficient Credit Balance"})
      
      resumeAnalyze = ResumeAnalyzer()
      response = resumeAnalyze.resumeSummarizer(app.config["UPLOAD_FOLDER"], email, fileId)

      subtract = calculate_scores_charges
      if "msg" in response.keys():
         subtract = 0
      credit_response = cred.substract_credits(email, subtract)

      return jsonify({"response": response, "credits": credit_response})
   
   except Exception as ex:
      print("Exception: ",ex.with_traceback)
      print(traceback.format_exc())
      return jsonify({"error": str(ex), "traceback": traceback.format_exc()})
   finally:
      cleanFolder()
      pass
   pass

app.add_url_rule("/summarize_resume", 'summarize_resume', summarize_resume, methods=methods)


def get_extracted_summary():
   try:

      email = request.get_json()['email']
      fileId = request.get_json()['fileId']
      resumeAnalyze = ResumeAnalyzer()
      response = resumeAnalyze.getExtractedSummary(fileId)
      return json.dumps(response)
   
   except Exception as ex:
      print("Exception: ",ex.with_traceback)
      print(traceback.format_exc())
      return jsonify({"error": str(ex), "traceback": traceback.format_exc()})
   finally:
      cleanFolder()
      pass
   pass

app.add_url_rule("/get_extracted_summary", 'get_extracted_summary', get_extracted_summary, methods=methods)

def extract_resume_metadata():
   try:

      email = request.get_json()['email']
      fileId = request.get_json()['fileId']

      cred = Credits()
      if not cred.check_sufficient_credit(email, extract_resume_metadata_charges):
         return jsonify({"msg": "Insufficient Credit Balance"})
      
      metadata = ResumeMetaData()
      response = json.loads(metadata.extractMetaData(app.config["UPLOAD_FOLDER"], email, fileId))

      subtract = calculate_scores_charges
      if "msg" in response.keys():
         subtract = 0
      
      credit_response = cred.substract_credits(email, subtract)

      return jsonify({"response": response, "credits": credit_response})
   
   except Exception as ex:
      print("Exception: ",ex.with_traceback)
      print(traceback.format_exc())
      return jsonify({"error": str(ex), "traceback": traceback.format_exc()})
   finally:
      cleanFolder()
      pass
   pass

app.add_url_rule("/extract_resume_metadata", 'extract_resume_metadata', extract_resume_metadata, methods=methods)

def get_extracted_keywords():
   try:

      email = request.get_json()['email']
      fileId = request.get_json()['fileId']
      metadata = ResumeMetaData()
      response = metadata.getExtractedKeywords(fileId)
      return json.dumps(response)
   
   except Exception as ex:
      print("Exception: ",ex.with_traceback)
      print(traceback.format_exc())
      return jsonify({"error": str(ex), "traceback": traceback.format_exc()})
   finally:
      cleanFolder()
      pass
   pass

app.add_url_rule("/get_extracted_keywords", 'get_extracted_keywords', get_extracted_keywords, methods=methods)


def login():
   try:
      email = request.get_json()['email']
      password = request.get_json()['password']
      
      login = LoginClass()
      result = login.userLogin(email, password)

      return json.dumps({"msg": result})
   
   except Exception as ex:
      print("Exception: ",ex.with_traceback)
      print(traceback.format_exc())
      return jsonify({"error": str(ex), "traceback": traceback.format_exc()})
   finally:
      cleanFolder()
      pass
   pass

app.add_url_rule("/login", 'login', login, methods=methods)


def logout():
   try:
      email = request.get_json()['email']
      
      login = LoginClass()
      result = login.userLogout(email)

      return json.dumps({"msg": result})
   
   except Exception as ex:
      print("Exception: ",ex.with_traceback)
      print(traceback.format_exc())
      return jsonify({"error": str(ex), "traceback": traceback.format_exc()})
   finally:
      cleanFolder()
      pass
   pass

app.add_url_rule("/logout", 'logout', logout, methods=methods)

def register():
   try:
      email = request.get_json()['email']
      password = request.get_json()['password']
      
      login = LoginClass()
      result = login.userRegister(email, password)

      return json.dumps({"msg": result})
   
   except Exception as ex:
      print("Exception: ",ex.with_traceback)
      print(traceback.format_exc())
      return jsonify({"error": str(ex), "traceback": traceback.format_exc()})
   finally:
      cleanFolder()
      pass
   pass

app.add_url_rule("/register", 'register', register, methods=methods)


def upload_files():
   try:

      fileMgmt = FileManagement()

      email = request.form['email']
      jdfiles = request.files.getlist("jdfiles")
      resumefiles = request.files.getlist("resfiles")

      jds_folder = os.path.join(app.config["UPLOAD_FOLDER"],email,"jds")

      res_foler = os.path.join(app.config["UPLOAD_FOLDER"],email,"resumes")

      if not os.path.exists(jds_folder):
         os.makedirs(jds_folder)
      elif not fileMgmt.ifFileUploadable(jds_folder):
         return json.dumps({"msg": "You have reached max upload capacity for Job Descriptions. Please delete existing JD files."})
      
      if not os.path.exists(res_foler):
         os.makedirs(res_foler)
      elif not fileMgmt.ifFileUploadable(res_foler):
         return json.dumps({"msg": "You have reached max upload capacity for Resumes. Please delete existing Resume files."})
      
      
      for file in jdfiles:
         if file.filename:
            filePath = os.path.join(jds_folder, file.filename)
            file.save(filePath)
            fileMgmt.uploadFile(file.filename, email, "jds")

      
      for file in resumefiles:
         if file.filename:
            filePath = os.path.join(res_foler, file.filename)
            file.save(filePath)
            fileMgmt.uploadFile(file.filename, email, "resumes")
      
      fileList = fileMgmt.getFileMetaList(email)

      return json.dumps({"msg": "Files uploaded Successfully", "Files": fileList})
   except Exception as ex:
      print("Exception: ",ex.with_traceback)
      print(traceback.format_exc())
      return jsonify({"error": str(ex), "traceback": traceback.format_exc()})
   finally:
      cleanFolder()
      pass
   pass

app.add_url_rule("/upload_files", 'upload_files', upload_files, methods=methods)


def delete_files():
   try:
      email = request.get_json()['email']
      fileId_list = request.get_json()['fileId_list']
      
      fileMgmt = FileManagement()

      folderPath = os.path.join(app.config["UPLOAD_FOLDER"],email)

      result = fileMgmt.deleteFiles(email, folderPath, fileId_list)

      folders = list(os.walk(app.config["UPLOAD_FOLDER"]))[1:]

      fileMgmt.emptyFolder(folders)

      return json.dumps({"msg": result})
   except Exception as ex:
      print("Exception: ",ex.with_traceback)
      print(traceback.format_exc())
      return jsonify({"error": str(ex), "traceback": traceback.format_exc()})
   finally:
      cleanFolder()
      pass
   pass

app.add_url_rule("/delete_files", 'delete_files', delete_files, methods=methods)


def get_file_list():
   try:
      email = request.get_json()['email']
      fileMgmt = FileManagement()

      fileList = fileMgmt.getFileMetaList(email)

      return json.dumps({"Files": fileList})

   except Exception as ex:
      print("Exception: ",ex.with_traceback)
      print(traceback.format_exc())
      return jsonify({"error": str(ex), "traceback": traceback.format_exc()})
   finally:
      cleanFolder()
      pass
   pass

app.add_url_rule("/get_file_list", 'get_file_list', get_file_list, methods=methods)


def download_file():
   email = request.get_json()['email']
   fileId = request.get_json()['fileId']

   fileMgmt = FileManagement()
   folderPath = os.path.join(app.config["UPLOAD_FOLDER"],email)
   filePath = fileMgmt.downloadFile(email, folderPath, fileId)
   
   return send_file(filePath)

app.add_url_rule("/download_file", 'download_file', download_file, methods=methods)

def get_credits():
   email = request.get_json()['email']
   cred = Credits()
   response = cred.get_credits(email)
   return jsonify(response)
   pass

app.add_url_rule("/get_credits", 'get_credits', get_credits, methods=methods)

def add_credits():
   email = request.get_json()['email']
   addCredits = int(request.get_json()['credits'])
   cred = Credits()
   response = cred.add_credits(email, addCredits)
   return jsonify(response)
   pass

app.add_url_rule("/add_credits", 'add_credits', add_credits, methods=methods)


if __name__ == '__main__':
   print("Getting things started !!")
   # app.run()
   run_with_ngrok(app)
   host = api_config['HOST']
   port = int(api_config['PORT'])
   ngrok_key = api_config['NGROK_KEY']
   ngrok.set_auth_token(ngrok_key)
   print(ngrok.connect(port).public_url)
   http_server = WSGIServer((host, port), app, spawn=10)
   print("~~~~~~~~~~~~~~~~~~~ Starting Server ~~~~~~~~~~~~~~~~~~~")
   http_server.serve_forever()
