import requests

# URL da API (ajuste se rodar em outro host/porta)
url = "http://127.0.0.1:8000/predict"

# Exemplo de dados de entrada
payload = {
    "NotaFinal": 7.5,
    "QuantidadeFaltasAnual": 10,
    "IDEB": 5.2,
    "TaxaEvasao": 0.1,
    "TaxaReprovacao": 0.05,
    "TaxaFaltas": 0.0,
    "MediaNotasAluno": 7.0,
    "ReprovacoesAcumuladas": 0,
    "RepetiuSerie": 0,
    "TaxaEvasaoCalc": 0.0
}

# Enviar requisição POST
response = requests.post(url, json=payload)

# Mostrar resultado
print("Status code:", response.status_code)
print("Resposta JSON:", response.json())