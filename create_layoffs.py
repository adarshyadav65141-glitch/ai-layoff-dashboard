import sqlite3
import pandas as pd
import pymysql

# 👉 MySQL connection (तुम्हारा original DB)
conn_mysql = pymysql.connect(
    host="localhost",
    user="root",
    password="2003",
    database="layoffs_db"
)

# 👉 MySQL से data fetch
df = pd.read_sql("SELECT * FROM layoffs", conn_mysql)

print("✅ MySQL Data Loaded:", len(df))

# 👉 SQLite DB बनाओ (cloud के लिए)
conn_sqlite = sqlite3.connect("layoffs.db")

# 👉 Table बनाओ
df.to_sql("layoffs", conn_sqlite, if_exists="replace", index=False)

conn_sqlite.close()

print("✅ SQLite DB Created with REAL DATA")