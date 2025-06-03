# requestes.py
import requests
from bs4 import BeautifulSoup
import json
import re  # Biblioteca para limpar os textos

# URLs das abas da Embrapa
URLS = {
    "producao": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02",
    "processamento": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03",
    "comercializacao": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04",
    "importacao": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05",
    "exportacao": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06"
}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def limpar_valores(valor):
    """Substitui valores '-' por '0' para evitar erros."""
    return valor if valor != "-" else "0"

def extrair_dados(url, nome_categoria):
    """Extrai os dados de cada aba do site e organiza em um dicionário."""
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        tabela = soup.find("table", class_="tb_base tb_dados") if nome_categoria == "importacao" else soup.find("table", class_="tb_dados")
        dados_extraidos = {}

        if tabela:
            linhas = tabela.find_all("tr")
            for linha in linhas:
                colunas = linha.find_all("td")
                dados = [coluna.text.strip() for coluna in colunas if coluna.text.strip()]
                
                if nome_categoria == "importacao" and len(dados) == 3:  # Importação tem 3 colunas
                    pais, volume, valor = dados
                    dados_extraidos[pais] = {"volume": limpar_valores(volume), "valor": limpar_valores(valor)}
                elif len(dados) == 2:  # Outras abas têm 2 colunas (Produto, Quantidade)
                    chave, valor = dados
                    dados_extraidos[chave] = limpar