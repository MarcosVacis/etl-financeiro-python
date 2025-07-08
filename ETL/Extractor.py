import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_income_statement(ticker, limit=5):
    api_key = os.getenv("FMP_API_KEY")
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit={limit}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao buscar dados de {ticker}: {response.status_code}")
        return []

