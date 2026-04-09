
import pandas as pd

layoffs = pd.read_csv("layoffs.csv")
skills = pd.read_csv("skills.csv")

# print("layoffs: ",layoffs['total_laid_off'].sum())#इससे तुम्हें पता चलेगा:
# ➡️ total कितने लोग निकाले गए

industry_data=layoffs.groupby('industry')['total_laid_off'].sum()
# print(industry_data)

year_data=layoffs.groupby('year')['total_laid_off'].sum()
# print(year_data)

ai_data=layoffs.groupby('ai_adopted')['total_laid_off'].sum()
# print(ai_data)

# print(skills['required_skills'].value_counts())

if year_data.idxmax() == 2023:
    print("Insight: Layoffs were highest in 2023")

if ai_data['Yes'] > ai_data['No']:
    print("Insight: AI adopted companies have more layoffs")
# Data → Analysis → Visualization → Insight ✅ yeh tak hum yeh sab kaam kiya hai
print("🚀 DB CODE START")

from db_connect import get_connection

try:
    print("STEP 1")
    conn = get_connection()

    print("STEP 2 - Connected")
    cursor = conn.cursor()

    print("STEP 3 - Cursor created")

    print("Total rows in DataFrame:", len(layoffs))

    print("INSERT PART STARTED")

    for index, row in layoffs.iterrows():
        print("Inserting:", row['company'])
        cursor.execute(
            "INSERT INTO layoffs (company, industry, total_laid_off, year, ai_adopted) VALUES (%s, %s, %s, %s, %s)",
            (row['company'], row['industry'], int(row['total_laid_off']), int(row['year']), row['ai_adopted'])
        )

    conn.commit()
    print("✅ Data Inserted Successfully!")

except Exception as e:
    print("❌ ERROR:", e)