import sqlite3
conn = sqlite3.connect("Tempus.db", isolation_level=None)
# 커서 획득
c = conn.cursor()
# 테이블 생성 (데이터 타입은 TEST, NUMERIC, INTEGER, REAL, BLOB 등)
c.execute("CREATE TABLE IF NOT EXISTS user \
    (email text PRIMARY KEY, name text, pnum text, address text, password text)")
# c.execute("INSERT INTO table1 \
#     VALUES(1, 'LEE', '1987-00-00')")
# c.execute("SELECT * FROM table1")
# print(c.fetchone())
#print(c.fetchone())
#print(c.fetchall())