import joblib
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

bundle = joblib.load("app/model/model.pkl")
model = bundle["model"]
preprocessor = bundle["preprocessor"]

class StudentData(BaseModel):
    NotaFinal: float
    QuantidadeFaltasAnual: int
    SituacaoAlunoTurma: str
    SituacaoAlunoDisciplina: str
    Descricao: str
    TurnoPrincipal: str
    TipoResponsavel: str
    IDEB: float
    TaxaEvasao: float
    TaxaReprovacao: float

@router.post("/predict")
def predict(data: StudentData):
    # Converte entrada em DataFrame
    df = pd.DataFrame([data.dict()])
    X = preprocessor.transform(df)
    prediction = model.predict_proba(X)[0][1]
    return {"defasagem_risco": round(float(prediction), 2)}