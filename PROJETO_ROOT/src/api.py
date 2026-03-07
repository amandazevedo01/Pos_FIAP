from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# 1. Inicializar API
app = FastAPI(title="Datathon Passos Mágicos - API")

# 2. Carregar modelo treinado
model = joblib.load("model.pkl")

# 3. Definir estrutura de entrada
class StudentData(BaseModel):
    NotaFinal: float
    QuantidadeFaltasAnual: float
    IDEB: float
    TaxaEvasao: float
    TaxaReprovacao: float
    TaxaFaltas: float = 0.0
    MediaNotasAluno: float = 0.0
    ReprovacoesAcumuladas: int = 0
    RepetiuSerie: int = 0
    TaxaEvasaoCalc: float = 0.0

# 4. Endpoint de previsão
@app.post("/predict")
def predict(data: StudentData):
    # Converter entrada para DataFrame
    df = pd.DataFrame([data.dict()])
    # Fazer previsão
    prediction = model.predict(df)[0]
    prob = model.predict_proba(df)[0].tolist()
    return {
        "DefasagemPrevista": int(prediction),
        "Probabilidades": {
            "Sem Defasagem": prob[0],
            "Com Defasagem": prob[1]
        }
    }