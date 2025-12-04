import pandas as pd
import requests

# Carregar os CSVs
emails = pd.read_csv("data/clean/emails.csv")
meetings = pd.read_csv("data/clean/meetings.csv")

# Testar alguns textos do CSV de emails
for text in emails["body"].head(5):   # supondo que a coluna seja 'body'
    response = requests.post(
        "http://127.0.0.1:8000/sentiment",
        json={"text": str(text)}
    )
    print("EMAIL:", text, "=>", response.json())

# Testar alguns textos do CSV de reuniões
for text in meetings["notes"].head(5):   # supondo que a coluna seja 'notes'
    response = requests.post(
        "http://127.0.0.1:8000/sentiment",
        json={"text": str(text)}
    )
    print("MEETING:", text, "=>", response.json())
