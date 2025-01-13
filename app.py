from flask import Flask, redirect, url_for, render_template, request, jsonify, send_file
from flask_cors import CORS
import simplejson as json
import os, time, traceback
import shutil
from src.mains.candidate_job_match import MatchJobCandidate
from src.mains.resume_analyzer import ResumeAnalyzer
from src.mains.resume_metadata import ResumeMetaData
from src.utils.upload_files import FileManagement
from src.mains.login import LoginClass
from flask_ngrok import run_with_ngrok
from pyngrok import ngrok
from gevent.pywsgi import WSGIServer
import warnings
warnings.filterwarnings("ignore")


os.environ['NGROK_AUTHTOKEN'] = "2jnVep6aB6LQiMXbLG9n05OqZ2R_2xPZMPXSpQc695dD9f36B"
os.environ['CUDA_LAUNCH_BLOCKING']="1"
os.environ['TORCH_USE_CUDA_DSA'] = "1"


app = Flask(__name__)
CORS(app=app)


cwd = os.getcwd()
app.config["ALLOWED_EXTENSIONS"] = [".pdf"]
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024 # 25 MB
app.config["UPLOAD_FOLDER"] = os.path.join(cwd, "data")

methods = ['POST']

def home():
   return render_template('index.html')

app.add_url_rule('/', 'home', home, methods=methods)

def calculate_scores():
   try:
      timestr = time.strftime("%Y%m%d_%H%M%S")
      jds_folder = os.path.join(app.config["UPLOAD_FOLDER"],timestr,"jds")
      os.makedirs(jds_folder)
      res_foler = os.path.join(app.config["UPLOAD_FOLDER"],timestr,"resumes")
      os.makedirs(res_foler)

      email = request.get_json()['email']

      fileUpload = FileManagement()

      jdfiles = request.files.getlist("jdfiles")
      for file in jdfiles:
         filePath = os.path.join(jds_folder, file.filename)
         file.save(filePath)
         fileUpload.uploadFile(file.filename, email)
      
      resumefiles = request.files.getlist("resfiles")
      for file in resumefiles:
         filePath = os.path.join(res_foler, file.filename)
         file.save(filePath)
         fileUpload.uploadFile(file.filename, email)
      
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
      shutil.rmtree(os.path.join(app.config["UPLOAD_FOLDER"],timestr), ignore_errors=False,)
   
app.add_url_rule("/calculate_scores", 'calculate_scores', calculate_scores, methods=methods)

def summarize_resume():
   try:
      timestr = time.strftime("%Y%m%d_%H%M%S")
      
      res_foler = os.path.join(app.config["UPLOAD_FOLDER"],timestr,"resumes")
      os.makedirs(res_foler)
      
      resumefiles = request.files.getlist("resfiles")
      for file in resumefiles:
         filePath = os.path.join(res_foler, file.filename)
         file.save(filePath)
      
      resumeAnalyze = ResumeAnalyzer()
      response = resumeAnalyze.resumeBatchSummarizer(res_foler)

      return json.dumps(response)
   
   except Exception as ex:
      print("Exception: ",ex.with_traceback)
      print(traceback.format_exc())
      return jsonify({"error": str(ex), "traceback": traceback.format_exc()})
   finally:
      shutil.rmtree(os.path.join(app.config["UPLOAD_FOLDER"],timestr), ignore_errors=False,)
   pass

app.add_url_rule("/summarize_resume", 'summarize_resume', summarize_resume, methods=methods)

def extract_resume_metadata():
   try:
      timestr = time.strftime("%Y%m%d_%H%M%S")
      
      res_foler = os.path.join(app.config["UPLOAD_FOLDER"],timestr,"resumes")
      os.makedirs(res_foler)
      
      resumefiles = request.files.getlist("resfiles")
      for file in resumefiles:
         filePath = os.path.join(res_foler, file.filename)
         file.save(filePath)
      
      metadata = ResumeMetaData()
      response = metadata.extractMetaData(res_foler)

      return json.dumps(response)
   
   except Exception as ex:
      print("Exception: ",ex.with_traceback)
      print(traceback.format_exc())
      return jsonify({"error": str(ex), "traceback": traceback.format_exc()})
   finally:
      shutil.rmtree(os.path.join(app.config["UPLOAD_FOLDER"],timestr), ignore_errors=False,)
   pass

app.add_url_rule("/extract_resume_metadata", 'extract_resume_metadata', extract_resume_metadata, methods=methods)

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
      pass
   pass

app.add_url_rule("/register", 'register', register, methods=methods)


def upload_files():
   try:
      email = request.get_json()['email']

      jds_folder = os.path.join(app.config["UPLOAD_FOLDER"],email,"jds")
      os.makedirs(jds_folder)

      res_foler = os.path.join(app.config["UPLOAD_FOLDER"],email,"resumes")
      os.makedirs(res_foler)
      
      fileMgmt = FileManagement()

      jdfiles = request.files.getlist("jdfiles")
      for file in jdfiles:
         filePath = os.path.join(jds_folder, file.filename)
         file.save(filePath)
         fileMgmt.uploadFile(file.filename, email)

      resumefiles = request.files.getlist("resfiles")
      for file in resumefiles:
         filePath = os.path.join(res_foler, file.filename)
         file.save(filePath)
         fileMgmt.uploadFile(file.filename, email)

      return json.dumps({"msg": "Files uploaded Successfully"})
   except Exception as ex:
      print("Exception: ",ex.with_traceback)
      print(traceback.format_exc())
      return jsonify({"error": str(ex), "traceback": traceback.format_exc()})
   finally:
      pass
   pass

app.add_url_rule("/upload_files", 'upload_files', upload_files, methods=methods)


def delete_files():
   try:
      email = request.get_json()['email']
      fileId_list = request.get_json()['fileId_list']
      fileName_list = request.get_json()['fileId_list']
      
      fileMgmt = FileManagement()

      filePathList = []
      jds_folder = os.path.join(app.config["UPLOAD_FOLDER"],email,"jds")
      for fileName in fileName_list:
         filePathList.append(os.path.join(jds_folder, fileName))

      fileMgmt.deleteFiles(fileId_list, filePathList)

      return json.dumps({"msg": "Files Deleted Successfully"})
   except Exception as ex:
      print("Exception: ",ex.with_traceback)
      print(traceback.format_exc())
      return jsonify({"error": str(ex), "traceback": traceback.format_exc()})
   finally:
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
      pass
   pass

app.add_url_rule("/get_file_list", 'get_file_list', get_file_list, methods=methods)


def download_file():
   email = request.get_json()['email']
   fileType = request.get_json()['fileType']
   fileName = request.get_json()['fileName']

   folder = None
   if fileType.lower() == 'jd':
      folder = os.path.join(app.config["UPLOAD_FOLDER"],email,"jds")
   
   if fileType.lower() == 'resume':
      folder = os.path.join(app.config["UPLOAD_FOLDER"],email,"resumes")
   
   
   return send_file(os.path.join(folder, fileName))

app.add_url_rule("/download_file", 'download_file', download_file, methods=methods)

if __name__ == '__main__':
   print("Getting things started !!")
   # app.run()
   run_with_ngrok(app)
   port=5000
   ngrok_key = "2jnVep6aB6LQiMXbLG9n05OqZ2R_2xPZMPXSpQc695dD9f36B"
   ngrok.set_auth_token(ngrok_key)
   ngrok.connect(port).public_url
   http_server = WSGIServer(("0.0.0.0", port), app)
   print("~~~~~~~~~~~~~~~~~~~ Starting Server ~~~~~~~~~~~~~~~~~~~")
   http_server.serve_forever()
