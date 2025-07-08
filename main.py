from ETL.Extractor import get_income_statement
from ETL.Transformer import transform_income_statement
from ETL.Loader import load_to_sqlite
import pandas as pd 
empresas = ["AAPL","MSFT", "AMZN"]

dfs = []  # Lista para armazenar os DataFrames

for ticker in empresas:
    raw_data = get_income_statement(ticker)
    df = transform_income_statement(raw_data, ticker)
    load_to_sqlite(df)
    dfs.append(df)  
    print(f"{ticker} carregado com sucesso.")

dados = pd.concat(dfs, ignore_index=True)  # Juntar todos os DataFrames
print(dados)

def salvarDados (df):
    try:
        df.to_csv(r"C:\Users\marco\Downloads\dadosparaDashboard.csv", sep=';', decimal=',' ,index=False)
        print ("Dados Salvo com sucesso")
    except Exception as e:
        print(f"Falha ao importar:{e} ")

salvarDados(dados) 