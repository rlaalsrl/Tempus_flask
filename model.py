# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import urllib.request
from collections import Counter
from konlpy.tag import Mecab
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, Dense, GRU
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from eunjeon import Mecab
#from keras.models import model_from_json 

# json_file = open("model.json", "r")
# loaded_model_json = json_file.read() 
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)
# model = Sequential()
# # model weight load 
# model.load_weights("model_weight.h5")

# model.compile(loss='categorical_crossentropy', optimizer=Adam(0.0000045), metrics=['accuracy'])
# train_score = model.evaluate(x_train, y_train, verbose=0)
# val_score = model.evaluate(x_val, y_val, verbose=0)
# total_mean_score = model.evaluate(x_total, y_total, verbose=0)
 
# print('training loss : ' + str(train_score[0]))
# print('validation loss : ' + str(val_score[0]))
 
# print('training accuracy : ' + str(train_score[1]))
# print('validation accuracy : ' + str(val_score[1]))
 
# print('total loss : ' + str(total_mean_score[0]))
# print('total accuracy : ' + str(total_mean_score[1]))



# total_data = pd.read_table('ratings_total.txt', names=['ratings', 'reviews'])
# #print('전체 리뷰 개수 :',len(total_data)) # 전체 리뷰 개수 출력
# total_data['label'] = np.select([total_data.ratings > 3], [1], default=0)
# #total_data[:5]
# total_data['ratings'].nunique(), total_data['reviews'].nunique(), total_data['label'].nunique()
# total_data.drop_duplicates(subset=['reviews'], inplace=True)
# train_data, test_data = train_test_split(total_data, test_size = 0.25, random_state = 42)
# train_data['reviews'] = train_data['reviews'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
# train_data['reviews'].replace('', np.nan, inplace=True)
# test_data.drop_duplicates(subset = ['reviews'], inplace=True) # 중복 제거
# test_data['reviews'] = test_data['reviews'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","") # 정규 표현식 수행
# test_data['reviews'].replace('', np.nan, inplace=True) # 공백은 Null 값으로 변경
# test_data = test_data.dropna(how='any') # Null 값 제거



# # train_data['tokenized'] = train_data['reviews'].apply(mecab.morphs)
# # train_data['tokenized'] = train_data['tokenized'].apply(lambda x: [item for item in x if item not in stopwords])
# # negative_words = np.hstack(train_data[train_data.label == 0]['tokenized'].values)
# # positive_words = np.hstack(train_data[train_data.label == 1]['tokenized'].values)
# # negative_word_count = Counter(negative_words)
# # positive_word_count = Counter(positive_words)
# # X_train = train_data['tokenized'].values
# # y_train = train_data['label'].values
# # X_test= test_data['tokenized'].values
# # y_test = test_data['label'].values

# # tokenizer.fit_on_texts(X_train)

# threshold = 2
# total_cnt = len(tokenizer.word_index) # 단어의 수
# rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
# total_freq = 0 # 훈련 데이터의 전체 단어 빈도수 총 합
# rare_freq = 0 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

# # 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
# for key, value in tokenizer.word_counts.items():
#     total_freq = total_freq + value

#     # 단어의 등장 빈도수가 threshold보다 작으면
#     if(value < threshold):
#         rare_cnt = rare_cnt + 1
#         rare_freq = rare_freq + value

# vocab_size = total_cnt - rare_cnt + 2
# tokenizer = Tokenizer(vocab_size, oov_token = 'OOV') 
# # tokenizer.fit_on_texts(X_train)
# # X_train = tokenizer.texts_to_sequences(X_train)
# # X_test = tokenizer.texts_to_sequences(X_test)
#urllib.request.urlretrieve("https://raw.githubusercontent.com/bab2min/corpus/master/sentiment/naver_shopping.txt", filename="ratings_total.txt")
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

sentiment_predict("작년에 군대 전역하고 나서이번 년도에 복학을 하게 되었습니다.그래서 원래 쓰던 L사의 사무용 노트북을 놔두고코딩 프로그램 사용이라던가 3d 작업을 요하는 경우가 많아져서이리저리 돌아다니다가 국내 최초 3070 탑재 노트북인 ASUS TUF FX516PR을 발견했습니다.일단 전체적인 스펙은 제품 상세설명에 기재되어 있는 것과 일치합니다. 매우 좋다는 뜻입니다, 여담으로 경첩 사이 공간에 표시등 들어오는 것에 취향저격 당해버렸습니다.전체적으로 봤을 때 디자인도 타사제품과 비교했을 때 세련되었고, 무엇보다도 초슬림에 경량까지 챙긴 노트북이기 때문에 같은 가격대에서도 쉽사리 볼 수 없는 그런 제품입니다.노트북 가방도 좋은 정품 asus 가방을 증정받았습니다. 잘 사용할게요!현재 아쉬운 점이 있는데 asus 자사 프로그램인 armoury crate에 aura sync가 아직 업데이트가 안 되었는지키보드 색의 변경이 아직은 불가능합니다. 차후에 업데이트 예정일 것으로 생각하기에(개인적인 바람입니다.)제품 지원 리스트 업데이트되고 나면 없어질 점이기 때문에 제 생각에는 현존 최강 가성비 3070 노트북이 아닐까 싶습니다. 휘황찬란하게 될 키보드를 생각하니 가슴이 웅장해집니다.많은 분들이 문의하거나 할 만한 사항이 있을텐데 노트북 구매 후 바이오스 세팅 및 바이오스와 드라이버 설치 및 툴 업그레이드는 구매 후 직접 하셔야 된다는 것을 인지해야 합니다.제품 구매 후 도움 되시라고 FX516PR 드라이버&툴 링크를 걸어두겠습니다.https://www.asus.com/kr/supportonly/FX516PR/HelpDesk_Download/그리고 대문짝만하게 제품상세 설명에도 쓰여있지만 쓰윽 읽고 넘어가시는 분들을 위해 한 가지 더 얘기할 것이 있습니다. Intel 11세대 프로세서(타이거레이크)를 탑재하고 있는 노트북이어서 윈도우 10 설치 시 IRST 드라이버를 로드 해주어야 합니다.상세 제품설명에도 쓰여있지만 참고로 링크를 걸어두겠습니다.https://www.asus.com/kr/support/FAQ/1044458//위 두 링크 모두 참고하셔서 행복하게 ASUS TUF FX516PR 사용하셨으면 좋겠습니다.이상 지나가던 대학생의 리뷰였습니다.")
