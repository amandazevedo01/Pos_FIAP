from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
import os
import matplotlib.pyplot as plt

app = FastAPI(title="Passos Mágicos - API de Previsão")

# Carregar modelo salvo
model = joblib.load("random_forest_model.pkl")

# Definir chave secreta a partir de variável de ambiente
SECRET_KEY = os.getenv("SECRET_KEY", "default_key")

# Definir formato de entrada
class StudentData(BaseModel):
    RA: Optional[str] = None
    Nome: Optional[str] = None
    Fase: str
    Turma: str
    Ano_nasc: int
    Idade_22: int
    Gênero: str
    Ano_ingresso: int
    Instituição_de_ensino: str
    Pedra_20: str
    Pedra_21: str
    Pedra_22: str
    INDE_22: float
    Cg: float
    Cf: float
    Ct: float
    N_Av: int
    Avaliador1: str
    Rec_Av1: str
    Avaliador2: str
    Rec_Av2: str
    Avaliador3: str
    Rec_Av3: str
    Avaliador4: str
    Rec_Av4: str
    IAA: float
    IEG: float
    IPS: float
    Rec_Psicologia: str
    IDA: float
    Matem: float
    Portug: float
    Inglês: float
    Atingiu_PV: str
    IPV: float
    IAN: float
    Fase_ideal: str
    Defas: str

@app.post("/batch_predict")
def batch_predict(data: List[StudentData]):
    try:
        df = pd.DataFrame([d.dict() for d in data])
        df = df.drop(columns=["RA", "Nome"], errors="ignore")

        # Codificar colunas categóricas
        categorical_cols = df.select_dtypes(include=["object"]).columns
        if len(categorical_cols) > 0:
            encoder = LabelEncoder()
            for col in categorical_cols:
                df[col] = encoder.fit_transform(df[col])

        # Previsões
        preds = model.predict(df)
        probs = model.predict_proba(df)[:, 1]

        results = []
        for i in range(len(data)):
            results.append({
                "RA": data[i].RA,
                "Nome": data[i].Nome,
                "Previsto": int(preds[i]),
                "Probabilidade_Indicado": float(probs[i])
            })

        # Salvar em CSV
        results_df = pd.DataFrame(results)
        results_df.to_csv(
            "predicoes.csv",
            mode="a",
            header=not os.path.exists("predicoes.csv"),
            index=False
        )

        return results
    except Exception as e:
        return {"erro": str(e)}

@app.get("/relatorio")
def relatorio():
    try:
        if not os.path.exists("predicoes.csv"):
            return {"mensagem": "Nenhum resultado salvo ainda."}

        df = pd.read_csv("predicoes.csv")

        # Contagem e percentuais
        contagem = df["Previsto"].value_counts().to_dict()
        total = len(df)
        percentuais = {classe: (qtd / total) * 100 for classe, qtd in contagem.items()}

        # Média das probabilidades
        media_prob = df["Probabilidade_Indicado"].mean()

        # Gráfico de pizza
        labels = [f"Classe {classe}" for classe in contagem.keys()]
        sizes = list(contagem.values())
        colors = ["#66b3ff", "#ff9999"]

        plt.figure(figsize=(6,6))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=140)
        plt.title("Distribuição das Previsões")
        plt.savefig("relatorio_pizza.png")
        plt.close()

        # Gráfico de barras
        plt.figure(figsize=(6,4))
        plt.bar(labels, sizes, color=colors)
        plt.title("Contagem de Previsões")
        plt.xlabel("Classe")
        plt.ylabel("Quantidade")
        plt.savefig("relatorio_barras.png")
        plt.close()

        relatorio = {
            "Total registros": total,
            "Contagem por classe": contagem,
            "Percentuais por classe (%)": percentuais,
            "Média probabilidade indicado": media_prob,
            "Graficos": {
                "Pizza": "/grafico/pizza",
                "Barras": "/grafico/barras"
            }
        }

        return relatorio
    except Exception as e:
        return {"erro": str(e)}

@app.get("/grafico/pizza")
def grafico_pizza():
    if os.path.exists("relatorio_pizza.png"):
        return FileResponse("relatorio_pizza.png")
    return {"mensagem": "Gráfico de pizza ainda não gerado."}

@app.get("/grafico/barras")
def grafico_barras():
    if os.path.exists("relatorio_barras.png"):
        return FileResponse("relatorio_barras.png")
    return {"mensagem": "Gráfico de barras ainda não gerado."}

@app.get("/download")
def download_csv():
    if os.path.exists("predicoes.csv"):
        return FileResponse("predicoes.csv", media_type="text/csv", filename="predicoes.csv")
    return {"mensagem": "Nenhum arquivo de previsões encontrado."}

@app.delete("/limpar")
def limpar_csv(secret: str = Query(..., description="Chave secreta para autorização")):
    try:
        if secret != SECRET_KEY:
            return {"erro": "Chave secreta inválida. Operação não autorizada."}

        if os.path.exists("predicoes.csv"):
            os.remove("predicoes.csv")
            return {"mensagem": "Arquivo predicoes.csv apagado com sucesso. Histórico reiniciado."}
        else:
            return {"mensagem": "Nenhum arquivo de previsões encontrado para apagar."}
    except Exception as e:
        return {"erro": str(e)}