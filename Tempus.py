from flask import Flask,request,jsonify,g
from flask import url_for, send_from_directory
import json
import os
from werkzeug.utils import secure_filename

#from pymongo import MongoClient

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
    	img_name = secure_filename(img.filename)
    	saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
    	img.save(saved_path)
    	return send_from_directory(app.config['UPLOAD_FOLDER'],img_name, as_attachment=True)
    else:
    	return "Iamge not found"


# @app.route('/mainboard')
# def send_mainboard():
#     im = Image.open('test.jpg')
#     return im



if __name__ == '__main__':
    app.run(host="192.168.0.3",debug=True)