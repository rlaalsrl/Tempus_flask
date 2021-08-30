from flask import Flask,request,jsonify,g,render_template
from flask import url_for, send_from_directory
import json
import os
from werkzeug.utils import secure_filename
import sqlite3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from eunjeon import Mecab
from collections import Counter
import tempfile
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
#from werkzeug import redirect
from flask.helpers import flash
from flask import send_file

app = Flask(__name__)


@app.route('/')
def home():
    return "hello"

@app.route('/board',methods=['HEAD','GET','POST'])
def send_board():
    jsonData = request.get_json()
    # try:
    #     f = open("board.txt",'r')
    #     Str = f.read()
    #     Str = '['+ Str + ']'
    #     print(Str)
    #     return Str
    #     f.close()
    # except:
    #     print("errer")
    # print(jsonData["email"])
    try:
        conn = sqlite3.connect("user_board.db", isolation_level=None)
        c = conn.cursor()
        c.execute("SELECT board FROM user_board WHERE name=:id",{"id":"kim"})
        
        # dit = c.fetchall()
        # data = {

        # 'text': dit       
        # }

        # jsondata = json.dumps(data)
        # load = json.loads(jsondata)
        
        # dit = c.fetchall()

        fw = open("temp.txt","w")
        for row in c.fetchall():
            row_str = str(row)
            data = { 
                'text': row_str 
                }
            fw.write(str(data)+',\n')
        fw.close()
        fw = open("temp.txt","r")
        load = fw.read()
        fw.close()


        board_list = '[' + str(load) + ']'
        return board_list
    except:
        print("errer")

@app.route('/imgdownload',methods=['HEAD','GET','POST'])
def imgsend():
    return send_file("C:/Users/real1/OneDrive/Desktop/Tempus_flask/test_img.jpg",mimetype='image/jpg')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host="192.168.0.3",debug=True)
