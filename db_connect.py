import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

# ✅ FIX: absolute path use करो (MOST IMPORTANT 🔥)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "data.db")

# ✅ FIX: function के अंदर connection + table create करो
def get_connection():
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()

    # ✅ table ensure (हर बार safe)
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

    return conn