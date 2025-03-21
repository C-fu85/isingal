# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, session, redirect, url_for
from flask import request as flask_request
from urllib.parse import unquote
from datetime import timedelta
import sys
from ivppepy.util import util

#from werkzeug.utils import secure_filename
#from ivp_util.web import flask_util
     
app = Flask(__name__)

UPLOAD_FOLDER = '/tmp/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours = 2)
@app.route("/", methods=['GET', 'POST'])
@app.route("/<f1>", methods=['GET', 'POST'])
def root(f1=''): 
    sso_userid, sso_username = check_sso()
    session['sso_id'] = sso_userid
    session['sso_name'] = sso_username
    
    if sso_userid == None:
        return "Error: please loging"
    
    if sso_userid not in admin_account:
        if f1 in ['']:
            f1 = 'index'
        elif f1 not in func_list:
            return ""
        #return "You have no right to enter the PED admin page!"
    else:
        if f1 in ['']:
            f1 = 'index_admin'
        elif f1 not in func_list:
            return ""
    
    if True:
        return eval("%s()"%(f1,))

def check_sso():
    sso_userid = flask_request.headers.get('sso-userid', None)
    sso_username = flask_request.headers.get('sso_chname', None)
    
    return sso_userid, sso_username

def allowed_file(filename):
    return True
    
@app.route("/main", methods=['GET', 'POST'])
def main():
    return "I am main."

@app.route("/index", methods=['GET', 'POST'])
def index():
    tid = session.get('sso_id')
    tname = unquote(session.get('sso_name'))
    
    return render_template('index.html', teacher_id=tid, teacher_name=tname)

@app.route("/index_admin", methods=['GET', 'POST'])
def index_admin():
    sso_id = session.get('sso_id')
    if sso_id is None:
        sso_id = ''
    #print(sso_id, file=sys.stderr)
    '''
    in_id = sso_id
    if flask_request.method == "POST":
        in_id = flask_request.form["account"]
        session['id'] = in_id
        if len(session['id']) == 9:
            return redirect("charts_stu")
        if len(session['id']) == 6:
            return redirect("charts")
    '''
    return render_template('index_admin.html', student_id = sso_id)

#charts for teacher
@app.route("/charts", methods=['GET', 'POST'])
def charts():
    tid = session.get('sso_id')
    return render_template('charts.html', account = tid)

#charts for student
@app.route("/charts_stu", methods=['GET', 'POST'])
def charts_stu():
    sid = session.get('sso_id')
    return render_template('charts_stu.html', account = sid)

@app.route("/letter", methods=['GET', 'POST'])
def letter():
    return render_template('letter.html')

def letter_p1():
    return render_template('letter_p1.html')

def letter_p2():
    return render_template('letter_p2.html')

def letter_p3():
    return render_template('letter_p3.html')

def P_mods():
    return render_template('P_mods.html')

@app.route("/charts_instructor", methods=['GET', 'POST']) 
def charts_compare():
    return render_template('charts_instructor.html')

@app.route("/charts_detail", methods=['GET', 'POST'])
def charts_detail():
    return render_template('charts_detail.html')

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('https://sso.tku.edu.tw/pkmslogout')

func_list = dir()

@app.route("/charts_ewant", methods=['GET', 'POST'])
def charts_ewant():
    return render_template('charts_ewant.html')

@app.route("/charts_ewant_2", methods=['GET', 'POST'])
def charts_ewant_2():
    return render_template('charts_ewant_2.html')
    
if __name__ == '__main__' :
    app.run(host='0.0.0.0', debug=True, port='6869')
   # app.run(host='0.0.0.0', debug=True, port='65324')
