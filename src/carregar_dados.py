from pathlib import Path
import pandas as pd
import sqlite3
from contextlib import closing

#Pathlib é para calcular a raiz do projeto a partir do próprio arquivo, roda de qualquer pasta
RAIZ = Path(__file__).parent.parent
CAMINHO_CSV = RAIZ / "data" / "entrada" / "vendas.csv"
CAMINHO_DB = RAIZ / "data" / "vendas.db" 

def carregar_csv(caminho_csv):
    return pd.read_csv(caminho_csv)
    

def salvar_no_banco(df, conexao):
    #Grava o data frame no banco de dados
    df.to_sql("vendas", conexao, if_exists="replace", index=False)

def verificar_banco(conexao):
    print(pd.read_sql("SELECT COUNT(*) AS total FROM vendas", conexao))
    print(pd.read_sql("SELECT * FROM vendas LIMIT 5", conexao))
    print(pd.read_sql("PRAGMA table_info(vendas)", conexao)) 

def main():
    df = carregar_csv(CAMINHO_CSV)

    with closing(sqlite3.connect(CAMINHO_DB)) as conexao:
        salvar_no_banco(df, conexao)
        verificar_banco(conexao)

if __name__ == "__main__": 
    main()