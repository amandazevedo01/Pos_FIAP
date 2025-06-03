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
    """Substitui valores '-' por '0' para evitar erros e mantém todos os países no JSON."""
    return valor.strip() if valor.strip() != "-" else "0"

def extrair_dados(url, nome_categoria):
    """Extrai os dados das tabelas da página e organiza em um dicionário."""
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Ajuste na captura da tabela de exportação e importação
        if nome_categoria in ["importacao", "exportacao"]:
            tabela = soup.find("table", class_="tb_base tb_dados")  # Confirmar se a classe está correta
        else:
            tabela = soup.find("table", class_="tb_dados")

        dados_extraidos = {}

        if tabela:
            linhas = tabela.find_all("tr")
            for linha in linhas:
                colunas = linha.find_all("td")
                dados = [coluna.text.strip() for coluna in colunas if coluna.text.strip()]
                
                if nome_categoria in ["importacao", "exportacao"] and len(dados) == 3:
                    pais, volume, valor = dados
                    dados_extraidos[pais] = {"volume": limpar_valores(volume), "valor": limpar_valores(valor)}
                elif len(dados) == 2:
                    chave, valor = dados
                    dados_extraidos[chave] = limpar_valores(valor)

            # Capturar total no rodapé (tfoot)
            rodape = tabela.find("tfoot")
            if rodape:
                total_linha = rodape.find_all("td")
                if len(total_linha) == 3:
                    total_volume = limpar_valores(total_linha[1].text.strip())
                    total_valor = limpar_valores(total_linha[2].text.strip())
                    dados_extraidos["Total"] = {"volume": total_volume, "valor": total_valor}

        else:
            print(f"🚨 Atenção! Nenhuma tabela encontrada em {url}. Pode haver mudanças na estrutura da página.")
        
        return dados_extraidos

    else:
        print(f"❌ Erro ao acessar a página {url}: {response.status_code}")
        return {}

# Extraindo e salvando os dados em JSON
for nome, url in URLS.items():
    print(f"🔍 Extraindo dados de {nome}...")
    dados = extrair_dados(url, nome)

    # Depuração: imprimir os primeiros itens do JSON gerado
    if dados:
        print(f"🔹 Primeiros itens extraídos de '{nome}':", list(dados.items())[:5])

    with open(f"dados_{nome}.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    print(f"✅ Arquivo 'dados_{nome}.json' criado com sucesso!\n")