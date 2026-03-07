from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()
model = joblib.load("app/model/best_model.pkl")

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    df = df.apply(pd.to_numeric, errors="coerce").fillna(0)
    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0,1] if len(model.classes_) > 1 else None
    return {"prediction": int(pred), "probability": float(prob) if prob is not None else None}