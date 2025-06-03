from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import re  # Biblioteca para limpar textos

app = FastAPI()

# Adicionando CORS para permitir requisições externas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite qualquer origem
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Função para carregar os dados do JSON
def carregar_dados(nome):
    try:
        with open(f"dados_{nome}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"mensagem": f"Arquivo dados_{nome}.json não encontrado."}

# Endpoint para consulta geral e filtragem por produto
@app.get("/{categoria}")
def obter_dados(
    categoria: str,
    produto: str = Query(None, description="Filtrar por produto específico")
):
    dados = carregar_dados(categoria)

    if not dados or isinstance(dados, dict) and not dados:  # Se o JSON estiver vazio
        return {"mensagem": f"Sem dados disponíveis para '{categoria}'."}

    if produto:
        produto_formatado = re.sub(r"[^\w\s]", "", produto.strip().lower())
        resultado_formatado = {re.sub(r"[^\w\s]", "", k.strip().lower()): v for k, v in dados.items()}

        # Busca parcial para encontrar produtos similares
        produtos_similares = {k: v for k, v in resultado_formatado.items() if produto_formatado in k}
        return {"dados": produtos_similares} if produtos_similares else {"mensagem": f"Produto '{produto}' não encontrado na categoria '{categoria}'."}

    return {"dados": dados}

# Página inicial da API
@app.get("/")
def read_root():
    return {"message": "✅ API funcionando!"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
