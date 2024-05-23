from flask import Flask, redirect, url_for, render_template, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app=app)


def home():
   return render_template('home.html')

app.add_url_rule('/', 'home', home)



if __name__ == '__main__':
   port=8080
   host="127.0.0.1"
   app.run(host=host,port=port)