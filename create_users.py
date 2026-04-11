import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# 🔥 users table create
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()
conn.close()

print("✅ users table created")