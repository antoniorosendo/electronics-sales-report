import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).parent.parent
PASTA_SRC = RAIZ / "src"

def executar_script(nome_script):
    print(f"\nIniciando: {nome_script}")
    caminho_script = PASTA_SRC / nome_script
    
    #Executa o script
    resultado = subprocess.run([sys.executable, str(caminho_script)])
    
    #Verifica se houve algum erro na execução
    if resultado.returncode != 0:
        print(f"Erro ao executar {nome_script}. Processo interrompido.")
        sys.exit(1)
        
    print(f"{nome_script} finalizado com sucesso!")

def main():
    #Imprime um letreiro com 50 '=' em volta
    print("="*50)
    print("PIPELINE DE RELATÓRIO DE VENDAS DE ELETRÔNICOS")
    print("="*50)
    
    #Executa os scripts na ordem exata do fluxo de dados
    executar_script("carregar_dados.py")
    executar_script("gerar_relatorio.py")
    executar_script("enviar_email.py")
    
    print("\n" + "="*50)
    print("AUTOMAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*50)

if __name__ == "__main__":
    main()