import sqlite3
import pandas as pd

# 👉 dummy data (तुम बाद में real डाल सकते हो)
data = {
    "company": ["Google", "Amazon", "Microsoft"],
    "year": [2023, 2023, 2022],
    "total_laid_off": [12000, 10000, 8000],
    "industry": ["Tech", "Tech", "Tech"],
    "ai_adopted": ["Yes", "No", "Yes"],
    "reason": ["AI Automation", "Cost Cutting", "Restructuring"]
}

df = pd.DataFrame(data)

conn = sqlite3.connect("data.db")

# 🔥 layoffs table create + data insert
df.to_sql("layoffs", conn, if_exists="replace", index=False)

conn.close()

print("✅ layoffs table created")