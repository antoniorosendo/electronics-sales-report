from pathlib import Path
import pandas as pd
import sqlite3
from contextlib import closing

#Pathlib é para calcular a raiz do projeto a partir do próprio arquivo, roda de qualquer pasta
RAIZ = Path(__file__).parent.parent
CAMINHO_DB = RAIZ / "data" / "vendas.db" 

def faturamento_total(conexao):
    consulta = "SELECT SUM (quantidade * preco) AS faturamento FROM vendas"
    return pd.read_sql(consulta, conexao).iloc[0, 0]

def ticket_medio(conexao):
    consulta = "SELECT SUM (quantidade * preco) / COUNT(DISTINCT id_pedido) AS ticket_medio FROM vendas"
    return pd.read_sql(consulta, conexao).iloc[0, 0]

def faturamento_por_mes(conexao):
    consulta = """SELECT strftime('%Y-%m', data) AS mes, 
    SUM(quantidade * preco) AS faturamento, 
    SUM(quantidade) AS itens, 
    COUNT(DISTINCT id_pedido) AS pedidos
    FROM vendas
    GROUP BY mes
    ORDER BY mes ASC
    """
    return pd.read_sql(consulta, conexao)

def faturamento_por_categoria(conexao):
    consulta = """SELECT categoria, SUM(quantidade * preco) AS faturamento
    FROM vendas
    GROUP BY categoria
    ORDER BY faturamento DESC
    """
    return pd.read_sql(consulta, conexao)

def faturamento_por_produto(conexao):
    consulta = """SELECT produto, SUM(quantidade * preco) AS faturamento
    FROM vendas
    GROUP BY produto
    ORDER BY faturamento DESC
    """
    return pd.read_sql(consulta, conexao)

def faturamento_por_vendedor(conexao):
    consulta = """SELECT vendedor, SUM(quantidade * preco) AS faturamento
    FROM vendas
    GROUP BY vendedor
    ORDER BY faturamento DESC
    """
    return pd.read_sql(consulta, conexao)

def melhor_mes(df):
    return df.sort_values("faturamento", ascending=False).iloc[0]

def melhor_produto(df):
    return df.sort_values("faturamento", ascending=False).iloc[0]

def melhor_vendedor(df):
    return df.sort_values("faturamento", ascending=False).iloc[0]

def calcular_indicadores(conexao):
    #Devolve todos os indicadores do relatório em um dicionário
    total = faturamento_total(conexao)
    ticket = ticket_medio(conexao)
    por_mes = faturamento_por_mes(conexao)
    por_categoria = faturamento_por_categoria(conexao)
    por_produto = faturamento_por_produto(conexao)
    por_vendedor = faturamento_por_vendedor(conexao)

    mes_top = melhor_mes(por_mes)
    produto_top = melhor_produto(por_produto)
    vendedor_top = melhor_vendedor(por_vendedor)

    return {
        "faturamento_total": float(total),
        "ticket_medio": float(ticket),
        "por_mes": por_mes,
        "por_categoria": por_categoria,
        "por_produto": por_produto,
        "por_vendedor": por_vendedor,
        "melhor_mes": {"nome": str(mes_top["mes"]), "faturamento": float(mes_top["faturamento"])},
        "melhor_produto": {"nome": str(produto_top["produto"]), "faturamento": float(produto_top["faturamento"])},
        "melhor_vendedor": {"nome": str(vendedor_top["vendedor"]), "faturamento": float(vendedor_top["faturamento"])}
    }


def main():
    with closing(sqlite3.connect(CAMINHO_DB)) as conexao:
        indicadores = calcular_indicadores(conexao)

    print(f"Faturamento total: R$ {indicadores['faturamento_total']:,.2f}")
    print(f"Ticket médio: R$ {indicadores['ticket_medio']:,.2f}")
    print(f"Melhor mês: {indicadores['melhor_mes']['nome']}")
    print(f"Melhor produto: {indicadores['melhor_produto']['nome']}")
    print(f"Melhor vendedor: {indicadores['melhor_vendedor']['nome']}")
    print(indicadores["por_categoria"])
        
if __name__ == "__main__":
    main()
    