import pandas as pd
import matplotlib.pyplot as plt

layoffs = pd.read_csv("layoffs.csv")

year_data = layoffs.groupby('year')['total_laid_off'].sum()

year_data.plot()
year_data.plot(marker='o')
plt.xticks(year_data.index)   # 👈 ये line add करो
plt.title("Layoffs by Year")
plt.xlabel("Year")
plt.ylabel("Total Laid Off")
#
ai_data = layoffs.groupby('ai_adopted')['total_laid_off'].sum()

ai_data.plot(kind='bar')
plt.title("AI vs Non-AI Layoffs")
plt.xlabel("AI Adopted")
plt.ylabel("Total Laid Off")
plt.show()
# plt.show()
