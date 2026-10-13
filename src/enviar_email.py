import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
import pandas as pd
import sqlite3
from contextlib import closing
from dotenv import load_dotenv

from indicadores import calcular_indicadores
from corpos_email import corpo_diretoria, corpo_marketing, corpo_financeiro


#Carrega os diretórios
RAIZ = Path(__file__).parent.parent
CAMINHO_DB = RAIZ / "data" / "vendas.db"
CAMINHO_RELATORIO = RAIZ / "data" / "saida" / "relatorio_vendas.xlsx"
CAMINHO_DESTINATARIOS = RAIZ / "data" / "entrada" / "destinatarios.xlsx"

#Carrega as variáveis do .env
load_dotenv(RAIZ / ".env")

#Chama os corpos dos e-mails
FUNCOES_CORPO = {
    "Diretoria": corpo_diretoria,
    "Marketing": corpo_marketing,
    "Financeiro": corpo_financeiro
}

def ler_destinatarios(caminho):
    df = pd.read_excel(caminho)
    return df.to_dict(orient="records")

def montar_corpo(indicadores, nome, setor):
    #Pega a função certa para o setor do funcionário
    funcao = FUNCOES_CORPO.get(setor)
    
    if not funcao:
        print(f"Setor '{setor}' desconhecido. Ignorando a geracao do corpo do e-mail.")
        return None
    
    return funcao(indicadores, nome)

def disparar_email(remetente, senha, destinatario, assunto, corpo, caminho_anexo):
    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = destinatario
    msg.set_content(corpo)

    #Lê e anexa o arquivo do excel
    with open(caminho_anexo, "rb") as f:
        dados_anexo = f.read()
        nome_arquivo = Path(caminho_anexo).name

    msg.add_attachment(
        dados_anexo,
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=nome_arquivo
    )

    #Conecta no servidor STP do Gmail e envia
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remetente, senha)
        smtp.send_message(msg)

def main():
    #Recebe as credenciais de login do Gmail
    remetente = os.getenv("GMAIL_USER")
    senha = os.getenv("GMAIL_APP_PASSWORD")

    if not remetente or not senha:
        print("Erro: Credenciais de e-mail não encontradas no arquivo .env.")
        return

    print("Calculando indicadores...")
    with closing(sqlite3.connect(CAMINHO_DB)) as conexao:
        indicadores = calcular_indicadores(conexao)

    print("Lendo destinatários...")
    try:
        destinatarios = ler_destinatarios(CAMINHO_DESTINATARIOS)
    except FileNotFoundError:
        print(f"Erro: O arquivo {CAMINHO_DESTINATARIOS} não foi encontrado.")
        return

    for dest in destinatarios:
        nome = dest["Nome"]
        email = dest["Email"]
        setor = dest["Setor"]

        print(f"Preparando e-mail para {nome} ({setor})...")
        
        corpo = montar_corpo(indicadores, nome, setor)
        
        if not corpo:
            continue
        
        assunto = f"Relatório de Vendas 2024-2025 - {setor}"
        
        try:
            disparar_email(remetente, senha, email, assunto, corpo, CAMINHO_RELATORIO)
            print(f"E-mail enviado com sucesso para {email}!")
        except Exception as erro:
            print(f"Falha ao enviar e-mail para {email}. Erro: {erro}")

if __name__ == "__main__":
    main()