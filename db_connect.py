import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

conn=sqlite3.connect("data.db",
childProcessError=False)
cursor=conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE,password TEXT)
""")
conn.commit()