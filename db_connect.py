import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

conn=sqlite3.connect("data.db",
check_same_thread=False)
cursor=conn.cursor()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS layoffs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    industry TEXT,
    year INTEGER,
    total_laid_off INTEGER,
    ai_adopted TEXT
)
""")
conn.commit()

