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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re
import xlsxwriter
import pandas as pd

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

def sentimentAnalysis():
    Data = request.get_json()
    print(Data)
    score=sentiment_predict(str(Data["input"]))
    if(score > 0.5):
        result="긍정 리뷰입니다."
    else:
        result="부정 리뷰입니다."
    return result

def productSearch(productname):
    options = Options()
    options.add_argument('headless'); # headless는 화면이나 페이지 이동을 표시하지 않고 동작하는 모드
    
    workbook = xlsxwriter.Workbook("C:/Users/real1/OneDrive/Desktop/Tempus_flask/xlsx/"+productname+'.xlsx')
    worksheet = workbook.add_worksheet()
    excel_row = 1

    worksheet.set_column('A:A', 40) # A 열의 너비를 40으로 설정
    worksheet.set_row(0,18) # A열의 높이를 18로 설정
    worksheet.set_column('B:B', 12) # B 열의 너비를 12로 설정
    worksheet.set_column('C:C', 60) # C 열의 너비를 60으로 설정

    worksheet.write(0, 0, '제품 모델명')
    worksheet.write(0, 1, '가격')
    worksheet.write(0, 2, '링크')
    # webdirver 설정(Chrome, Firefox 등)
    # chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=options) # 브라우저 창 안보이기
    # driver = webdriver.Chrome() # 브라우저 창 보이기
    
    # 크롬 브라우저 내부 대기 (암묵적 대기)
    driver.implicitly_wait(5)
    
    # 브라우저 사이즈
    driver.set_window_size(1920,1280)

    driver.get('https://shopping.naver.com/home/p/index.naver')# 네이버 쇼핑 메인창
    xpath2 = "/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/div[1]/form/fieldset/div[1]/input[1]"
    search = driver.find_element_by_name("query")
    search.clear()
    search.send_keys(productname)
    time.sleep(1)
    search.send_keys("\n")
    time.sleep(2)
    
    # 현재 페이지
    curPage = 1
    
    # 크롤링할 전체 페이지수
    totalPage = 1
    
    while curPage <= totalPage:
        #bs4 초기화
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    
        # 상품 리스트 선택
        goods_list = soup.select('li.basicList_item__2XT81')
    
        # 페이지 번호 출력
        print('----- Current Page : {}'.format(curPage), '------')
    
        for v in goods_list:
            # 상품명, 가격, 이미지
            
            name = v.select_one('div.basicList_title__3P9Q7 > a').text.strip()
            price = v.select_one('span.price_num__2WUXn').text.strip()
            review_link = v.select_one('div.basicList_title__3P9Q7 > a').get('href')
            price = str(price).replace(',','')
            price = price.replace('원','') 
            print(name,', ', price, ', ', review_link)
            worksheet.write(excel_row, 0, name)
            worksheet.write(excel_row, 1, int(price))
            worksheet.write(excel_row, 2, review_link)



            driver.get(review_link)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            review_list = soup.select('p.reviewItems_text__XIsTc')
           
            for r in review_list:

                r.text.strip()
                r = str(r)
                r.replace('<br/>','')
                r = re.sub('<.+?>','',r,0).strip()
                print(r)
                worksheet.write(excel_row,3,r)
                print()
            excel_row += 1
            driver.back()
        
        
        time.sleep(5)
        print()
        # 페이지 수 증가
        curPage += 1
    
        if curPage > totalPage:
            print('Crawling succeed!')
            break
    
        # 페이지 이동 클릭
        cur_css = 'a.pagination_next__1ITTf'
        WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CSS_SELECTOR,cur_css))).click()
    
        #2,3페이지까지 확인할경우 과한 리소스 소모+추천 제품에서 멀어져 정확도 감소-> 1페이지만 검색함

        # BeautifulSoup 인스턴스 삭제
        del soup
    
        # 3초간 대기
        time.sleep(3)
    
    # 브라우저 종료
    workbook.close()
    driver.close()    

def prdctRcmnd(prdctname):
    productSearch(prdctname)
    data = pd.read_excel("C:/Users/real1/OneDrive/Desktop/Tempus_flask/xlsx/"+prdctname+".xlsx", engine="openpyxl",thousands = ',')
    data = data.sort_values(by="가격")
    with pd.ExcelWriter("C:/Users/real1/OneDrive/Desktop/Tempus_flask/xlsx/"+prdctname+"_sort.xlsx",engine="openpyxl") as writer:
        data.to_excel(writer,sheet_name="sheet1",index=False)
        

if __name__ == '__main__':
    prdctRcmnd("화장품")