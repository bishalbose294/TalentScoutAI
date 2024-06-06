from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_cors import CORS
import simplejson as json
import os, pathlib, time, traceback
import shutil
from src.mains.candidate_job_match import MatchJobCandidate
from src.mains.resume_analyzer import ResumeAnalyzer

app = Flask(__name__)
CORS(app=app)

cwd = os.getcwd()
app.config["ALLOWED_EXTENSIONS"] = [".pdf"]
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024 # 25 MB
app.config["UPLOAD_FOLDER"] = os.path.join(cwd, "uploads")

methods = ['GET','POST']

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
      return jsonify({"error": str(ex)})
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
      return jsonify({"error": str(ex)})
   finally:
      shutil.rmtree(os.path.join(app.config["UPLOAD_FOLDER"],timestr), ignore_errors=False,)
   pass

app.add_url_rule("/summarize_resume", 'summarize_resume', summarize_resume, methods=methods)

if __name__ == '__main__':
   port=8080
   host="127.0.0.1"
   app.run(host=host,port=port,debug=False)