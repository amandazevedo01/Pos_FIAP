📘 Projeto Datathon – Previsão de Defasagem Escolar
🎯 Visão Geral
Este projeto foi desenvolvido para apoiar a Associação Passos Mágicos na missão de transformar a vida de crianças e jovens por meio da educação.
O objetivo é construir um modelo preditivo capaz de estimar o risco de defasagem escolar de cada estudante, permitindo que professores e gestores tomem decisões mais assertivas.

🛠️ Stack Tecnológica
- Linguagem: Python 3.9
- Frameworks de ML: scikit-learn, pandas, numpy
- API: FastAPI
- Serialização: joblib
- Testes: pytest
- Empacotamento: Docker
- Deploy: Local (Docker) / Cloud (Heroku, AWS, GCP)
- Monitoramento: logging + relatórios automáticos


📂 Estrutura do Projeto
project-root/
├── app/
│   ├── __init__.py
│   └── main.py              # Código principal da API
├── src/
│   ├── preprocessing.py     # Funções de limpeza e preparação
│   ├── feature_engineering.py # Engenharia de atributos
│   ├── train.py             # Treinamento do modelo
│   ├── evaluate.py          # Avaliação e métricas
│   └── utils.py             # Funções auxiliares
├── tests/
│   ├── test_api.py          # Testes da API
│   ├── test_preprocessing.py# Testes de pré-processamento
│   └── test_model.py        # Testes do modelo
├── random_forest_model.pkl  # Modelo treinado
├── requirements.txt         # Dependências
├── Dockerfile               # Empacotamento da API
└── README.md                # Documentação

🚀 Instruções de Deploy
Pré-requisitos
- Python 3.9+
- Docker instalado
Instalação local
pip install -r requirements.txt
uvicorn app.main:app --reload



pip install -r requirements.txt
uvicorn app.main:app --reload

DOCKER
docker build -t fiap-mod5-api .
docker run -d -p 8000:8000 fiap-mod5-api
A API estará disponível em:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs



📊 Exemplos de Chamadas à API
Previsão em lote
curl -X POST "http://127.0.0.1:8000/batch_predict" \
-H "Content-Type: application/json" \
-d '[
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
    "IAA": 7.2,
    "IEG": 6.8,
    "IPS": 7.0,
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
]'

Relatórios e gráficos
- GET /relatorio → Estatísticas gerais
- GET /grafico/pizza → Gráfico de pizza
- GET /grafico/barras → Gráfico de barras
- GET /download → Baixar CSV com previsões

🧪 Testes
Rodar testes unitários:
pytest --maxfail=1 --disable-warnings -q


Com relatório de cobertura:
pytest --cov=app --cov=src tests/
🔎 Etapas da Pipeline de ML
- Pré-processamento dos dados
- Engenharia de features
- Treinamento e validação
- Seleção do modelo (Random Forest)
- Deploy via FastAPI + Docker
- Monitoramento com logs e relatórios
🎥 Entrega Final
- Código-fonte organizado e documentado.
- API funcional com endpoints de previsão e relatórios.
- Dockerfile para empacotamento.
- Testes unitários com Pytest.
- Documentação (README.md).
- Vídeo de até 5 minutos mostrando a solução.
