from flask import Flask,request,jsonify,g
from flask import url_for, send_from_directory
import json
import os
from werkzeug.utils import secure_filename
import sqlite3

#from pymongo import MongoClient
def json_trans(jsondata):
    strjson = str(jsondata).replace("[","")
    strjson = strjson.replace("]","") 
    return strjson

app = Flask(__name__)



@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/addboard',methods=['HEAD','GET','POST'])
def addpost():
    #print(request.is_json)
    jsonData = request.get_json()
    print(jsonData)
    #print(jsonData[0]['Title'])
    f = open("board.txt",'a')
    strjson = str(jsonData).replace("[","")
    strjson = strjson.replace("]","") 
    f.write(strjson+',\n')
    f.close()
    return 'ok'

@app.route('/board')
def send_board():
    f = open("board.txt",'r')
    #Str = f.readlines()
    Str = f.read()
    Str = '['+ Str + ']'
    print(Str)
    # S=0
    # for S in range(len(Str)):
    #     return Str[S]
    #print(Str)
    #return Str[1]
    #for j in range(jsons):
    #jsons = json.loads(Str.replace("'", "\""))
    #print(jsons)
    #print(jsons['Author'])
    #return json.dumps(jsons)
    return Str
    f.close()

@app.route('/imgupload',methods=['HEAD','GET','POST'])

def imgupload():
    if request.method == 'POST' and request.files['image']:
        
        img = request.files['image']
        img_name = secure_filename(img.filename)#key값으로 이름변경
        #saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        img.save()
        #return send_from_directory(app.config['UPLOAD_FOLDER'],img_name, as_attachment=True)
        return "Image receive"
    else:
        return "Image not found"


@app.route('/login',methods=['HEAD','GET','POST'])
def login():
    jsonData = request.get_json()
    auth = 'error'
    try:
        conn = sqlite3.connect("Tempus.db", isolation_level=None)
        c = conn.cursor()
        #print(val)
        param1=jsonData["email"]
        param2=jsonData["password"]
        #c.execute("SELECT * FROM user")
        c.execute("SELECT * FROM user WHERE email=:id and password=:pw",{"id":jsonData["email"],"pw":jsonData["password"]})
        #c.execute("SELECT * FROM user WHERE email=? and password=?",param1,param2)
        if c.fetchall()==[]:
            auth='error'
            print("null")
        else:
            auth='ok'
            print("ok")
        
    except:
        # c.execute("SELECT * FROM user")
        # print(c.fetchall())
        auth='error'
        print("error")
    #print(jsonData)
    # json_loginstring = jsonData['email']
    #print(jsonData["email"])
    return auth

@app.route('/signup',methods=['HEAD','GET','POST'])
def signup():
    jsonData = request.get_json()
    problem = "ok"
    #print(jsonData)
    try:
        conn = sqlite3.connect("Tempus.db", isolation_level=None)
        c = conn.cursor()
        val = [jsonData["email"],jsonData["name"],jsonData["pnum"],jsonData["address"],jsonData["password"]]
        #print(val)
        c.execute("INSERT INTO user \
            VALUES(?,?,?,?,?)", val)
        c.execute("SELECT * FROM user")
        print(c.fetchall())  
    except:
        problem = "error"
        print("error")
    # json_loginstring = jsonData['email']
    # print(jsonData["email"])
    return problem


if __name__ == '__main__':
    app.run(host="192.168.0.3",debug=True)