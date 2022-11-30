from flask import Flask, render_template,request
from topic_modelling import Topic_modeling
from summarizer import Summarizer
from summarizer.sbert import SBertSummarizer
import sqlite3
import pandas as pd
import numpy as np

#create an instance of the SBERT
model = SBertSummarizer('paraphrase-MiniLM-L6-v2')

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route("/signup")
def signup():
    
    
    name = request.args.get('username','')
    number = request.args.get('number','')
    email = request.args.get('email','')
    password = request.args.get('psw','')

    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `detail` (`name`,`number`,`email`, `password`) VALUES (?, ?, ?, ?)",(name,number,email,password))
    con.commit()
    con.close()

    return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('name','')
    password1 = request.args.get('psw','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `name`, `password` from detail where `name` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()
    print(data)

    if data == None:
        return render_template("signup.html")    

    # elif mail1 == 'admin' and password1 == 'admin':
    #     return render_template("index.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("index.html")
    else:
        return render_template("signup.html")


@app.route("/summarize",methods=['POST','GET'])
def getSummary():
    body=request.form['data']
    result = model(body, num_sentences=2)
    data = [result]
    df = pd.DataFrame({'sentence':data})
    t,word = Topic_modeling(df)

    return render_template('summary.html',result=result,to = t, wo = word)


@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/logon')
def reg():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')


if __name__ =="__main__":
    app.run(port=8000)
