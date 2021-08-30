import sqlite3
import json
conn = sqlite3.connect("user_board.db", isolation_level=None)
# 커서 획득
c = conn.cursor()
# 테이블 생성 (데이터 타입은 TEST, NUMERIC, INTEGER, REAL, BLOB 등)
c.execute("CREATE TABLE IF NOT EXISTS user_board \
    (id integer PRIMARY KEY autoincrement, name text, board text)")
# c.execute("INSERT INTO table1 \
#     VALUES(1, 'LEE', '1987-00-00')")
# c.execute("SELECT * FROM table1")
# print(c.fetchone())
#print(c.fetchone())
#print(c.fetchall())
# c.execute("Insert INTO user_board (name,board) VALUES('kim', '지하철 동호회')")
# c.execute("select * FROM user_board")
# print(c.fetchall())

c.execute("SELECT board FROM user_board WHERE name=:id",{"id":"kim"})
# print(c.fetchall())
dit = c.fetchall()
print(dit)
data = {

    'board': dit       
}
print(data)
jsondata = json.dumps(data)
print(jsondata)
load = json.loads(jsondata)
print(load)
jsondata2 =json.dumps(load)
print(jsondata2)
# db-> json 변환 필요
# print(type(jsondata))
# jsondata = json.dump(c.execute,'w')
# print(c.fetchall())
# print(jsondata)