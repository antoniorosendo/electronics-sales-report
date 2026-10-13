def formatar_reais(valor):
    #Formata um número como moeda brasileira (ex: R$ 20.000,00)
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"