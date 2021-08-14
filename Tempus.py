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


total_data = pd.read_table('ratings_total.txt', names=['ratings', 'reviews'])
total_data['label'] = np.select([total_data.ratings > 3], [1], default=0)
total_data['ratings'].nunique(), total_data['reviews'].nunique(), total_data['label'].nunique()
total_data.drop_duplicates(subset=['reviews'], inplace=True)

train_data, test_data = train_test_split(total_data, test_size = 0.25, random_state = 42)
train_data['reviews'] = train_data['reviews'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
train_data['reviews'].replace('', np.nan, inplace=True)
test_data.drop_duplicates(subset = ['reviews'], inplace=True) # 중복 제거
test_data['reviews'] = test_data['reviews'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","") # 정규 표현식 수행
test_data['reviews'].replace('', np.nan, inplace=True) # 공백은 Null 값으로 변경
test_data = test_data.dropna(how='any') # Null 값 제거
mecab = Mecab()

stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게']
train_data['tokenized'] = train_data['reviews'].apply(mecab.morphs)
train_data['tokenized'] = train_data['tokenized'].apply(lambda x: [item for item in x if item not in stopwords])
test_data['tokenized'] = test_data['reviews'].apply(mecab.morphs)
test_data['tokenized'] = test_data['tokenized'].apply(lambda x: [item for item in x if item not in stopwords])
max_len = 80
negative_words = np.hstack(train_data[train_data.label == 0]['tokenized'].values)
positive_words = np.hstack(train_data[train_data.label == 1]['tokenized'].values)
negative_word_count = Counter(negative_words)
positive_word_count = Counter(positive_words)
text_len = train_data[train_data['label']==1]['tokenized'].map(lambda x: len(x))
text_len = train_data[train_data['label']==0]['tokenized'].map(lambda x: len(x))
X_train = train_data['tokenized'].values
y_train = train_data['label'].values
X_test= test_data['tokenized'].values
y_test = test_data['label'].values
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)

threshold = 2
total_cnt = len(tokenizer.word_index) # 단어의 수
rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
total_freq = 0 # 훈련 데이터의 전체 단어 빈도수 총 합
rare_freq = 0 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

# 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
for key, value in tokenizer.word_counts.items():
    total_freq = total_freq + value

    # 단어의 등장 빈도수가 threshold보다 작으면
    if(value < threshold):
        rare_cnt = rare_cnt + 1
        rare_freq = rare_freq + value

vocab_size = total_cnt - rare_cnt + 2

tokenizer = Tokenizer(vocab_size, oov_token = 'OOV') 
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)

X_train = pad_sequences(X_train, maxlen = max_len)
X_test = pad_sequences(X_test, maxlen = max_len)


loaded_model = load_model('best_model.h5')
loaded_model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])


#from pymongo import MongoClient
def json_trans(jsondata):
    strjson = str(jsondata).replace("[","")
    strjson = strjson.replace("]","") 
    return strjson

def sentiment_predict(new_sentence):
    new_sentence = mecab.morphs(new_sentence) # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
    score = float(loaded_model.predict(pad_new)) # 예측
    if(score > 0.5):
        print("{:.2f}% 확률로 긍정 리뷰입니다.".format(score * 100))
    else:
        print("{:.2f}% 확률로 부정 리뷰입니다.".format((1 - score) * 100))
    return score


app = Flask(__name__)



@app.route('/')
def home():

    return render_template('C:/Users/real1/OneDrive/Desktop/Tempus_flask/upload.html')

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
    jsonData = request.get_json()
    try:
    # f = open("board.txt",'r')
    # #Str = f.readlines()
    # Str = f.read()
    # Str = '['+ Str + ']'
    # print(Str)
    # # S=0
    # # for S in range(len(Str)):
    # #     return Str[S]
    # #print(Str)
    # #return Str[1]
    # #for j in range(jsons):
    # #jsons = json.loads(Str.replace("'", "\""))
    # #print(jsons)
    # #print(jsons['Author'])
    # #return json.dumps(jsons)
    # return Str
    # f.close()
        conn = sqlite3.connect("user_board.db", isolation_level=None)
        c = conn.cursor()
        c.execute("SELECT * FROM user_board WHERE email=:id",{"id":jsonData["email"]})
        return c.fetchall
    except:
        print("errer")

@app.route('/imgupload',methods=['GET','POST'])
def imgupload():

    file = request.files["uploadedfile"]
    file.save("C:/Users/real1/OneDrive/Desktop/Tempus_flask/"+secure_filename(file.filename))

    return "업로드 성공"




    # if request.method == 'POST':
        
    #     if 'file' not in request.files:
    #         flash('No file part')
    #         #return redirect(request.url)
    #     f= request.files['file']
    #     if f:
    #         f.save(secure_filename(f.filename))
    #         f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
    #         return "Success"
    # else:
    #     return "Welcome to server"
        
        
        
        
        # file = request.files["image0"]
        # file.save("C:/Users/real1/OneDrive/Desktop/Tempus_flask/"+secure_filename(file.filename))

        # raw_data = request.get_data()
        # file = request.files['/storage/emulated/0/Pictures/photos/JPEG_20210705_162145.jpg']
        # print(raw_data)
        # print(file)
        # file.save("C:/Users/real1/OneDrive/Desktop/Tempus_flask/"+secure_filename(file.filename))


        #file.save(os.path.join("uploads",file.filename))

        # f = request.FILES['file']#f에 none값 해결부터
        # #저장할 경로 + 파일명
        # f.save('C:/Users/real1/OneDrive/Desktop/Tempus_flask/test.jpg')
        # files = os.listdir("./uploads")
        # return render_template('check.html')
        # img = request.files.get('image/jpg')
        # img_name = secure_filename("test")#key값으로 이름변경
        # #saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        # try:
        #     img.save(saved_path)
        # except AttributeError:
        #     print("Couldn't save image")
        # #return send_from_directory(app.config['UPLOAD_FOLDER'],img_name, as_attachment=True)
    #     return "파일 업로드 성공"
    # else:
    #     return "Image not found"



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


@app.route('/sentimentAnalysis',methods=['HEAD','GET','POST'])
def sentimentAnalysis():
    Data = request.get_json()
    print(Data)
    score=sentiment_predict(str(Data["input"]))
    if(score > 0.5):
        result="긍정 리뷰입니다."
    else:
        result="부정 리뷰입니다."
    return result

    


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host="192.168.0.3",debug=True)

# board 액티비티 - 현재는 게시판명을 제외한 나머지만 서버에 전달하지만, 게시판명도 게시판을 구분하기 위해 서버에 전달이 필요할듯
# (현재 게시판명은 board main에서 board, content 액티비티에 intent로 전달해서 사용 중)
# - 이하 변수들은 모두 board, content 액티비티에서 사용
# - WR_ID : 유저를 구분할 유저번호 또는 닉네임
# - WR_TYPE : 일반/지출목록 형식 구분
# - WR_DATE : 작성일자
# - WR_BODY : 글 내용
# - GROUP : 게시판명
# - 게시글 번호(현재는 추가 안되어있으나 추후 검색 기능을 추가했을 때 필요할 예정)


# content 액티비티에서만 사용하는 변수 - 모두 서버와 통신 필요
# - 댓글 작성자명
# - 댓글 내용
# - 댓글 작성 일자

# user_boar

# 기본키는 랜덤변수, 나머지는 email과 그룹명으로 구성된 db를 생성