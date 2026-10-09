import random
from datetime import date

import pandas as pd

#Garante que os dados gerados sejam sempre os mesmos
random.seed(42)

#Catálogo de produtos
produtos = [
    {"produto": "Notebook Básico", "categoria": "Computadores", "preco": 2500.00},
    {"produto": "Notebook Intermediário", "categoria": "Computadores", "preco": 4000.00},
    {"produto": "Notebook Gamer", "categoria": "Computadores", "preco": 7000.00},

    {"produto": "Mouse Básico", "categoria": "Periféricos", "preco": 60.00},
    {"produto": "Mouse Gamer", "categoria": "Periféricos", "preco": 180.00},
    {"produto": "Mouse Ergonômico", "categoria": "Periféricos", "preco": 220.00},
    {"produto": "Teclado Mecânico", "categoria": "Periféricos", "preco": 250.00},
    {"produto": "Teclado de Membrana", "categoria": "Periféricos", "preco": 100.00},
    {"produto": "Teclado Sem Fio", "categoria": "Periféricos", "preco": 180.00},

    {"produto": "Headphone Básico", "categoria": "Áudio", "preco": 100.00},
    {"produto": "Headphone Bluetooth", "categoria": "Áudio", "preco": 250.00},
    {"produto": "Headset Gamer", "categoria": "Áudio", "preco": 350.00},
    {"produto": "Earbuds", "categoria": "Áudio", "preco": 200.00},
    {"produto": "Caixa de Som Bluetooth", "categoria": "Áudio", "preco": 180.00},

    {"produto": "Impressora Jato de Tinta", "categoria": "Impressão", "preco": 500.00},
    {"produto": "Impressora Multifuncional", "categoria": "Impressão", "preco": 800.00},
    {"produto": "Impressora Laser", "categoria": "Impressão", "preco": 1200.00},
    {"produto": "Impressora Fotográfica", "categoria": "Impressão", "preco": 900.00},

    {"produto": "Smartphone Básico", "categoria": "Smartphones", "preco": 800.00},
    {"produto": "Smartphone Intermediário", "categoria": "Smartphones", "preco": 1300.00},
    {"produto": "Smartphone Avançado", "categoria": "Smartphones", "preco": 3500.00},
    {"produto": "Smartphone 5G", "categoria": "Smartphones", "preco": 2500.00},

    {"produto": "Carregador USB-C", "categoria": "Acessórios", "preco": 100.00},
    {"produto": "Carregador Sem Fio", "categoria": "Acessórios", "preco": 150.00},
    {"produto": "Cabo USB-C", "categoria": "Acessórios", "preco": 50.00},
    {"produto": "Adaptador USB", "categoria": "Acessórios", "preco": 70.00},

    {"produto": "SSD 1TB", "categoria": "Armazenamento", "preco": 500.00},
    {"produto": "HD Externo", "categoria": "Armazenamento", "preco": 300.00},
    {"produto": "Pendrive", "categoria": "Armazenamento", "preco": 80.00},
]

vendedores = [
    "Bruno",
    "João",
    "Maria",
    "Pedro",
    "Sabrina",
    "Vinicius",
]

#Período das vendas
data_inicio = date(2024, 1, 1)
data_fim = date(2025, 12, 31)

def obter_fator_sazonalidade(data):
    #Black Friday
    if data.month == 11 and data.weekday() == 4 and data.day >= 23:
        return 6.0

    #Black Friday Week
    if data.month == 11 and 24 <= data.day <= 30:
        return 3.0

    #Período de Natal
    if data.month == 12 and data.day <= 24:
        return 1.8

    #Volta às aulas
    if (data.month == 1 and data.day >= 15) or (data.month == 2 and data.day <= 15):
        return 1.5

    #Período normal
    return 1.0

def gerar_datas():
    return pd.date_range(
        start=data_inicio,
        end=data_fim,
        freq="D"
    )

def gerar_pesos_datas(datas):
    return [
        obter_fator_sazonalidade(data.date())
        for data in datas
    ]

def gerar_datas_pedidos(quantidade_pedidos, datas, pesos):
    return random.choices(
        datas,
        weights=pesos,
        k=quantidade_pedidos
    )

#Limites estabelecidos
quantidade_pedidos = 5000
datas = gerar_datas()
pesos = gerar_pesos_datas(datas)

datas_pedidos = gerar_datas_pedidos(
    quantidade_pedidos,
    datas,
    pesos
)

def gerar_quantidade_produtos():
    return random.randint(1, 4)

def selecionar_produtos(quantidade):
    return random.sample(produtos, quantidade)

def gerar_quantidade():
    return random.randint(1, 3)

def gerar_vendas(datas_pedidos):
    linhas_vendas = []

    for id_pedido, data in enumerate(datas_pedidos, start=1):
        vendedor = random.choice(vendedores)

        quantidade_produtos = gerar_quantidade_produtos()
        produtos_pedido = selecionar_produtos(quantidade_produtos)

        for produto in produtos_pedido:
            linha = {
                "id_pedido": id_pedido,
                "data": data,
                "produto": produto["produto"],
                "categoria": produto["categoria"],
                "vendedor": vendedor,
                "quantidade": gerar_quantidade(),
                "preco": produto["preco"]
            }

            linhas_vendas.append(linha)

    return linhas_vendas

#Cria as vendas de produtos e armazena em um data frame
linhas_vendas = gerar_vendas(datas_pedidos)
df = pd.DataFrame(linhas_vendas)

df.to_csv(
    "data/entrada/vendas.csv",
    index=False
)

print("Arquivo vendas.csv gerado com sucesso!")