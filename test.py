from main import extrair_dados

url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06"
nome_categoria = "exportacao"

dados = extrair_dados(url, nome_categoria)
print(dados)  # Verifica se os dados estão sendo extraídos corretamente