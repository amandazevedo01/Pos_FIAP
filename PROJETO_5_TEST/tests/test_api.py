from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_batch_predict_endpoint():
    payload = [
        {
            "Fase": "1",
            "Turma": "A",
            "Ano_nasc": 2005,
            "Idade_22": 20,
            "Gênero": "Masculino",
            "Ano_ingresso": 2023,
            "Instituição_de_ensino": "FIAP",
            "Pedra_20": "Azul",
            "Pedra_21": "Verde",
            "Pedra_22": "Amarela",
            "INDE_22": 0.75,
            "Cg": 7.5,
            "Cf": 8.0,
            "Ct": 7.8,
            "N_Av": 3,
            "Avaliador1": "Prof1",
            "Rec_Av1": "Sim",
            "Avaliador2": "Prof2",
            "Rec_Av2": "Não",
            "Avaliador3": "Prof3",
            "Rec_Av3": "Sim",
            "Avaliador4": "Prof4",
            "Rec_Av4": "Não",
            "IAA": 7.2,
            "IEG": 6.8,
            "IPS": 7.0,
            "Rec_Psicologia": "Não",
            "IDA": 6.9,
            "Matem": 8.5,
            "Portug": 7.0,
            "Inglês": 6.5,
            "Atingiu_PV": "Sim",
            "IPV": 7.4,
            "IAN": 6.7,
            "Fase_ideal": "1",
            "Defas": "Não"
        }
    ]
    response = client.post("/batch_predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Previsto" in data[0]
    assert "Probabilidade_Indicado" in data[0]