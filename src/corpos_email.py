from indicadores import calcular_indicadores
from formatacao import formatar_reais

def corpo_diretoria(indicadores, nome):
    melhor_mes = indicadores["melhor_mes"]
    melhor_produto = indicadores["melhor_produto"]
    produto_mais_vendido = indicadores["produto_mais_vendido"]
    melhor_vendedor = indicadores["melhor_vendedor"]

    corpo = f"""
Olá, {nome}!

Segue o resumo dos resultados de vendas no período de 2024 a 2025 para análise da Diretoria.

DESEMPENHO GERAL
- Faturamento total: {formatar_reais(indicadores['faturamento_total'])}
- Ticket médio: {formatar_reais(indicadores["ticket_medio"])}

DESTAQUES
- Melhor mês: {melhor_mes["nome"]}
- Faturamento do melhor mês: {formatar_reais(melhor_mes["faturamento"])}
- Melhor vendedor: {melhor_vendedor["nome"]}
- Faturamento do melhor vendedor: {formatar_reais(melhor_vendedor["faturamento"])}
- Produto com maior faturamento: {melhor_produto["nome"]}
- Faturamento do melhor produto: {formatar_reais(melhor_produto["faturamento"])}
- Produto mais vendido: {produto_mais_vendido["nome"]} ({produto_mais_vendido["unidades"]} unidades)

O relatório completo com todos os gráficos e detalhes está anexado a este e-mail.

Atenciosamente,
Antonio Carlos Rosendo da Silva
Analista de Inteligência Comercial
"""
    return corpo.strip()

def corpo_marketing(indicadores, nome):
    melhor_produto = indicadores["melhor_produto"]
    produto_mais_vendido = indicadores["produto_mais_vendido"]

    df_categoria = indicadores["por_categoria"]
    melhor_categoria_nome = df_categoria.iloc[0]["categoria"]
    melhor_categoria_faturamento = df_categoria.iloc[0]["faturamento"]

    corpo = f"""
Olá, {nome}!

Segue o resumo dos resultados de vendas no período de 2024 a 2025 para análise da equipe de Marketing.

DESTAQUES DE PRODUTOS E CATEGORIAS
- Produto mais vendido em unidades: {produto_mais_vendido["nome"]} ({produto_mais_vendido["unidades"]} unidades)
- Produto com maior faturamento: {melhor_produto["nome"]} ({formatar_reais(melhor_produto["faturamento"])})
- Categoria com maior faturamento: {melhor_categoria_nome} ({formatar_reais(melhor_categoria_faturamento)})

SUGESTÕES PARA CAMPANHAS
- O alto volume de vendas do {produto_mais_vendido["nome"]} indica que ele tem forte apelo para atrair clientes. Pode ser estratégico usá-lo como "produto de entrada" ou em promoções casadas com itens de maior valor agregado.
- O {melhor_produto["nome"]} foi o líder em geração de receita. Campanhas focadas na valorização dos diferenciais deste produto têm potencial para maximizar ainda mais o retorno financeiro.
- Como a categoria {melhor_categoria_nome} apresentou o maior faturamento, pode ser interessante explorar tendências desse segmento para ações futuras e alocação de orçamento.

O relatório completo com todos os gráficos e detalhes está anexado a este e-mail.

Atenciosamente,
Antonio Carlos Rosendo da Silva
Analista de Inteligência Comercial
"""
    return corpo.strip()

def corpo_financeiro(indicadores, nome):
    faturamento_total = indicadores["faturamento_total"]
    ticket_medio = indicadores["ticket_medio"]
    melhor_mes = indicadores["melhor_mes"]

    df_categoria = indicadores["por_categoria"]
    linhas_categorias = []
    for index, row in df_categoria.iterrows():
        nome_categoria = row["categoria"]
        fat_categoria = formatar_reais(row["faturamento"])
        linhas_categorias.append(f"- {nome_categoria}: {fat_categoria}")
    
    texto_categorias = "\n".join(linhas_categorias)

    corpo = f"""
Olá, {nome}!

Segue o resumo dos resultados financeiros de vendas referentes ao período de 2024 a 2025 para análise.

DESEMPENHO FINANCEIRO GERAL
- Faturamento total: {formatar_reais(faturamento_total)}
- Ticket médio: {formatar_reais(ticket_medio)}
- Melhor mês: {melhor_mes["nome"]} com {formatar_reais(melhor_mes["faturamento"])}

FATURAMENTO POR CATEGORIA
{texto_categorias}

O relatório completo, contendo o detalhamento mensal e os gráficos, está anexado a este e-mail.

Atenciosamente,
Antonio Carlos Rosendo da Silva
Analista de Inteligência Comercial
"""
    return corpo.strip()