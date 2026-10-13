from openpyxl import Workbook
from pathlib import Path
import sqlite3
from contextlib import closing
from indicadores import calcular_indicadores
from openpyxl.chart import LineChart, BarChart, Reference
from openpyxl.styles import Alignment

RAIZ = Path(__file__).parent.parent
PASTA_SAIDA = RAIZ / "data" / "saida"
PASTA_SAIDA.mkdir(parents=True, exist_ok=True)
CAMINHO_RELATORIO = PASTA_SAIDA / "relatorio_vendas.xlsx"
CAMINHO_DB = RAIZ / "data" / "vendas.db"

def preencher_resumo(aba, indicadores):
    aba.append(["Indicador", "Valor"])

    #Lista de tuplas
    linhas = [
        ("Faturamento total", indicadores["faturamento_total"], True),
        ("Ticket médio", indicadores["ticket_medio"], True),
        ("Melhor mês", indicadores["melhor_mes"]["nome"], False),
        ("Faturamento do melhor mês", indicadores["melhor_mes"]["faturamento"], True),
        ("Melhor produto", indicadores["melhor_produto"]["nome"], False),
        ("Faturamento do melhor produto", indicadores["melhor_produto"]["faturamento"], True),
        ("Produto mais vendido", indicadores["produto_mais_vendido"]["nome"], False),
        ("Quantidade do produto mais vendido", indicadores["produto_mais_vendido"]["unidades"], False),
        ("Melhor vendedor", indicadores["melhor_vendedor"]["nome"], False),
        ("Faturamento do melhor vendedor", indicadores["melhor_vendedor"]["faturamento"], True),
    ]

    #Desempacota cada tupla em três variáveis
    for rotulo, valor, e_dinheiro in linhas:
        aba.append([rotulo, valor]) #Adiciona na planilha
        celula = aba.cell(row=aba.max_row, column=2)
        celula.alignment = Alignment(horizontal="right")
        if e_dinheiro:
            celula.number_format = '"R$" #,##0.00' #Aplica a formatação da moeda

    #Ajusta a largura das colunas
    aba.column_dimensions["A"].width = 28
    aba.column_dimensions["B"].width = 18

def gerar_relatorio(indicadores, caminho_saida):
    wb = Workbook()
    resumo = wb.active
    resumo.title = "Resumo"
    mensal = wb.create_sheet("Mensal")
    categorias = wb.create_sheet("Categorias")
    produtos = wb.create_sheet("Produtos (Faturamento)")
    quantidade = wb.create_sheet("Produtos (Quantidade)")
    vendedores = wb.create_sheet("Vendedores")

    #Tabelas
    preencher_resumo(resumo, indicadores)
    escrever_tabela(mensal, indicadores["por_mes"])
    escrever_tabela(categorias, indicadores["por_categoria"])
    escrever_tabela(produtos, indicadores["por_produto"])
    escrever_tabela(quantidade, indicadores["por_quantidade"], colunas_dinheiro=())
    escrever_tabela(vendedores, indicadores["por_vendedor"])

    #Gráficos
    criar_grafico_linha(mensal, indicadores["por_mes"])
    criar_grafico_barras(categorias, indicadores["por_categoria"], "Faturamento por Categoria", "Categoria")
    criar_grafico_barras(produtos, indicadores["por_produto"], "Faturamento por Produto", "Produto")
    criar_grafico_barras(quantidade, indicadores["por_quantidade"], "Quantidade por Produto", "Produto", titulo_valor="Unidades vendidas", formato_valor="0")
    criar_grafico_barras(vendedores, indicadores["por_vendedor"], "Faturamento por Vendedor", "Vendedor")

    wb.save(caminho_saida)
    return caminho_saida

def escrever_tabela(aba, df, colunas_dinheiro=(2,)):
    df = df.rename(columns={"mes": "Mês", "faturamento": "Faturamento", "itens": "Itens", "pedidos": "Pedidos",
                            "categoria": "Categoria", "produto": "Produto", "vendedor": "Vendedor"})

    aba.append(list(df.columns))
    for linha in df.itertuples(index=False):
        aba.append(list(linha))

    for i in range(2, aba.max_row + 1):
        for coluna in colunas_dinheiro:
            aba.cell(row=i, column=coluna).number_format = '"R$" #,##0.00'

    aba.column_dimensions["A"].width = 28
    aba.column_dimensions["B"].width = 18

def criar_grafico_linha(aba, df):
    ultima_linha = len(df) + 1 #+1 por causa do cabeçalho

    grafico = LineChart()
    grafico.title = "Faturamento por mês"
    grafico.x_axis.title = "Mês"
    grafico.y_axis.title = "Faturamento (R$)"

    valores = Reference(aba, min_col=2, min_row=1, max_row=ultima_linha)
    meses = Reference(aba, min_col=1, min_row=2, max_row=ultima_linha)

    grafico.add_data(valores, titles_from_data=True)
    grafico.set_categories(meses)

    COR = "1F4E78" #azul escuro

    #Títulos fora da área do gráfico
    grafico.title.overlay = False
    grafico.x_axis.title.overlay = False
    grafico.y_axis.title.overlay = False

    #Define a linha como uma cor só e uma bolinha em cada mês
    grafico.varyColors = False
    serie = grafico.series[0]
    serie.smooth = False
    serie.graphicalProperties.line.solidFill = COR
    serie.graphicalProperties.line.width = 28575 #Espessura, em EMU (≈ 2,25 pt)
    serie.marker.symbol = "circle"
    serie.marker.size = 7
    serie.marker.graphicalProperties.solidFill = COR
    serie.marker.graphicalProperties.line.solidFill = COR

    #Sem legenda na direita
    grafico.legend = None

    grafico.x_axis.delete = False
    grafico.y_axis.delete = False

    grafico.y_axis.number_format = '"R$" #,##0'

    grafico.width = 24
    grafico.height = 11

    aba.add_chart(grafico, "F2")

def criar_grafico_barras(aba, df, titulo, titulo_categoria, titulo_valor="Faturamento (R$)", formato_valor='"R$" #,##0'):
    ultima_linha = len(df) + 1

    grafico = BarChart()
    grafico.title = titulo
    grafico.x_axis.title = titulo_categoria
    grafico.y_axis.title = titulo_valor

    valores = Reference(aba, min_col=2, min_row=1, max_row=ultima_linha)
    categorias = Reference(aba, min_col=1, min_row=2, max_row=ultima_linha)

    grafico.add_data(valores, titles_from_data=True)
    grafico.set_categories(categorias)

    COR = "1F4E78" #azul escuro

    #Títulos fora da área do gráfico
    grafico.title.overlay = False
    grafico.x_axis.title.overlay = False
    grafico.y_axis.title.overlay = False

    #Estilização do gráfico
    grafico.type = "bar"
    grafico.varyColors = False
    serie = grafico.series[0]
    serie.graphicalProperties.solidFill = COR

    #Resultados aparecem em ordem crescente
    grafico.x_axis.scaling.orientation = "maxMin"
    grafico.y_axis.crosses = "max"

    #Sem legenda na direita
    grafico.legend = None

    grafico.x_axis.delete = False
    grafico.y_axis.delete = False

    grafico.y_axis.number_format = formato_valor

    grafico.width = 24
    grafico.height = max(11, len(df) * 0.6) #Cresce com o número de itens
    grafico.x_axis.tickLblSkip = 1

    aba.add_chart(grafico, "D2")

def main():
    with closing(sqlite3.connect(CAMINHO_DB)) as conexao:
        indicadores = calcular_indicadores(conexao)
    caminho = gerar_relatorio(indicadores, CAMINHO_RELATORIO)
    print(f"Relatório gerado em: {caminho}")

if __name__ == "__main__":
    main()