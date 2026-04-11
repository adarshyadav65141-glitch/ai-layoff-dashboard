import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

conn=sqlite3.connect("data.db",
check_same_thread=False)
cursor=conn.cursor()
cursor.execute("SELECT COUNT(*) FROM layoffs")
count = cursor.fetchone()[0]

if count == 0:
    cursor.executemany("""
    INSERT INTO layoffs (company, location, industry, total_laid_off, year, ai_adopted)
    VALUES (?, ?, ?, ?, ?, ?)
    """, [
        ("Google", "USA", "Tech", 12000, 2023, "Yes"),
        ("Amazon", "USA", "E-commerce", 18000, 2023, "Yes"),
        ("Meta", "USA", "Tech", 11000, 2022, "Yes"),
        ("StartupX", "India", "Tech", 500, 2024, "No")
    ])
    conn.commit()