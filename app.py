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

db_config = config['DATABASE']

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
   fileMgmt = FileManagement()
   folders = list(os.walk(app.config["UPLOAD_FOLDER"]))[1:]
   fileMgmt.emptyFolder(folders)
   pass

def calculate_scores():
   try:

      fileUpload = FileManagement()

      email = request.form['email']

      jds_folder = os.path.join(app.config["UPLOAD_FOLDER"],email,"jds")

      

      res_foler = os.path.join(app.config["UPLOAD_FOLDER"],email,"resumes")
      
      if not os.path.exists(res_foler):
         os.makedirs(res_foler)
      elif not fileUpload.ifFileUploadable(res_foler):
         return json.dumps({"msg": "You have reached max upload capacity. Please delete existing files."})


      jdfiles = request.files.getlist("jdfiles")
      for file in jdfiles:
         if file.filename:
            filePath = os.path.join(jds_folder, file.filename)
            file.save(filePath)
            fileId = fileUpload.uploadFile(file.filename, email, "jds")
      
      resumefiles = request.files.getlist("resfiles")
      for file in resumefiles:
         if file.filename:
            filePath = os.path.join(res_foler, file.filename)
            file.save(filePath)
            fileUpload.uploadFile(file.filename, email, "resumes")
      
      match = MatchJobCandidate()
      pointers = match.generatePointers(jds_folder, res_foler)
      keywords = match.extractJDResumeKeywords(jds_folder, res_foler)

      final_dict = dict()

      for jd, resumePointers in pointers.items():
         temp_dict = dict()
         for resume, points in resumePointers.items():
            temp_dict[resume] = {
               'points' : points,
               'keywords' : keywords[jd][resume],
            }
         final_dict[jd] = temp_dict

      return json.dumps(final_dict)
   
   except Exception as ex:
      print("Exception: ",ex.with_traceback)
      print(traceback.format_exc())
      return jsonify({"error": str(ex), "traceback": traceback.format_exc()})
   finally:
      cleanFolder()
      pass
   
app.add_url_rule("/calculate_scores", 'calculate_scores', calculate_scores, methods=methods)

def summarize_resume():
   try:

      email = request.get_json()['email']
      fileId = request.get_json()['fileId']
      
      resumeAnalyze = ResumeAnalyzer()
      response = resumeAnalyze.resumeSummarizer(app.config["UPLOAD_FOLDER"], email, fileId)

      return json.dumps(response)
   
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
      
      metadata = ResumeMetaData()
      response = json.loads(metadata.extractMetaData(app.config["UPLOAD_FOLDER"], email, fileId))

      return json.dumps(response)
   
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
      
      jdfiles = request.files.getlist("jdfiles")
      for file in jdfiles:
         if file.filename:
            filePath = os.path.join(jds_folder, file.filename)
            file.save(filePath)
            fileMgmt.uploadFile(file.filename, email, "jds")

      resumefiles = request.files.getlist("resfiles")
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
   return json.loads(response)
   pass

app.add_url_rule("/get_credits", 'get_credits', get_credits, methods=methods)

def add_credits():
   email = request.get_json()['email']
   addCredits = request.get_json()['credits']
   cred = Credits()
   response = cred.add_credits(email, addCredits)
   return json.loads(response)
   pass

app.add_url_rule("/add_credits", 'add_credits', add_credits, methods=methods)

def subtract_credits():
   email = request.get_json()['email']
   subCredits = request.get_json()['credits']
   cred = Credits()
   response = cred.substract_credits(email, subCredits)
   return json.loads(response)
   pass

app.add_url_rule("/subtract_credits", 'subtract_credits', subtract_credits, methods=methods)

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
