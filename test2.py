import requests
from bs4 import BeautifulSoup

url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Capturar todo o conteúdo da tabela correta
tabela = soup.find("table", class_="tb_base tb_dados")

if tabela:
    print(tabela.prettify())  # Exibe toda a estrutura da tabela no terminal
else:
    print("❌ Tabela não encontrada.")


print(soup.prettify())  # Mostra todo o HTML da página