from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
from joblib import load

# Cria a aplicação FastAPI
app = FastAPI(title="TSLA LSTM API", description="Previsão de preços da Tesla com LSTM")

# Carrega modelo e scaler
model = tf.keras.models.load_model("artifacts/lstm_tsla_model.keras")
scaler = load("artifacts/price_scaler.joblib")

# Estrutura de entrada
class PriceData(BaseModel):
    prices: list  # lista de preços históricos (últimos 60 dias)

@app.post("/predict")
def predict(data: PriceData):
    seq = np.array(data.prices).reshape(-1, 1)
    seq_scaled = scaler.transform(seq)
    X_input = seq_scaled.reshape(1, seq_scaled.shape[0], 1)
    pred_scaled = model.predict(X_input)
    pred_real = scaler.inverse_transform(pred_scaled)
    return {"prediction": float(pred_real[0][0])}