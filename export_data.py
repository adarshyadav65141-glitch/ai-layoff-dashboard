import pymysql
import pandas as pd

# MySQL connection
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="2003",
    database="layoffs_db"
)

# 👉 पूरा data fetch करो
df = pd.read_sql("SELECT * FROM layoffs", conn)

# 👉 CSV में save करो
df.to_csv("layoffs.csv", index=False)

print("✅ Data exported to CSV")