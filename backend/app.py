from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_cors import CORS
import simplejson as json
import os, time, traceback
import shutil
from src.mains.candidate_job_match import MatchJobCandidate
from src.mains.resume_analyzer import ResumeAnalyzer
from src.mains.resume_metadata import ResumeMetaData
from flask_ngrok import run_with_ngrok
from pyngrok import ngrok
from gevent.pywsgi import WSGIServer


os.environ['NGROK_AUTHTOKEN'] = "2jnVep6aB6LQiMXbLG9n05OqZ2R_2xPZMPXSpQc695dD9f36B"
os.environ['CUDA_LAUNCH_BLOCKING']="1"
os.environ['TORCH_USE_CUDA_DSA'] = "1"


app = Flask(__name__)
CORS(app=app)


cwd = os.getcwd()
app.config["ALLOWED_EXTENSIONS"] = [".pdf"]
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024 # 25 MB
app.config["UPLOAD_FOLDER"] = os.path.join(cwd, "uploads")

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


      jdfiles = request.files.getlist("jdfiles")
      for file in jdfiles:
         filePath = os.path.join(jds_folder, file.filename)
         file.save(filePath)
      
      resumefiles = request.files.getlist("resfiles")
      for file in resumefiles:
         filePath = os.path.join(res_foler, file.filename)
         file.save(filePath)
      
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


if __name__ == '__main__':
   print("Getting things started !!")
   app.run()
   # run_with_ngrok(app)
   # port=5000
   # ngrok_key = "2jnVep6aB6LQiMXbLG9n05OqZ2R_2xPZMPXSpQc695dD9f36B"
   # ngrok.set_auth_token(ngrok_key)
   # ngrok.connect(port).public_url
   # http_server = WSGIServer(("0.0.0.0", port), app)
   # print("~~~~~~~~~~~~~~~~~~~ Starting Server ~~~~~~~~~~~~~~~~~~~")
   # http_server.serve_forever()
