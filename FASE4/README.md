📘 README – Projeto Previsão de Preços da Tesla com LSTM
📌 Visão Geral
Este projeto utiliza uma rede neural LSTM para prever o preço das ações da Tesla (TSLA) com base em séries temporais.
O modelo foi treinado com dados históricos, salvo em artefatos e disponibilizado via API FastAPI.

📂 Estrutura do Projeto
FASE4/
│── artifacts/
│   ├── lstm_tsla_model.keras
│   ├── price_scaler.joblib
│── api_tsla.py
│── notebook_treinamento.ipynb
│── README.md


- artifacts/ → contém o modelo e o scaler salvos.
- api_tsla.py → API FastAPI para servir previsões.
- notebook_treinamento.ipynb → código de treino e avaliação do modelo.
- README.md → documentação do projeto.

⚙️ Instalação
- Clone ou baixe o repositório.
- Crie um ambiente virtual (opcional, mas recomendado):
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
- Instale as dependências:
pip install -r requirements.txt


- Principais pacotes:
- fastapi
- uvicorn
- tensorflow
- numpy
- joblib
- pydantic
🚀 Executando a APINo terminal, dentro da pasta do projeto:uvicorn api_tsla:app --reload
Se tudo estiver correto, você verá:Uvicorn running on http://127.0.0.1:8000
🌐 EndpointsDocumentação interativa- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
Endpoint /predict- Método: POST
- Entrada (JSON):
{
  "prices": [720.5, 725.3, 730.1, ..., 1015.2]  // 60 valores consecutivos
}
- Saída (JSON):
{
  "prediction": 874.81
}
📊 Treinamento do Modelo- Rede LSTM com camadas recorrentes e densas.
- Janela de 60 dias para prever o próximo valor.
- Normalização dos dados com MinMaxScaler.
- Métricas utilizadas: MSE, RMSE.
- Modelo salvo em artifacts/lstm_tsla_model.keras.
✅ Checklist de Entrega- [x] Dados históricos tratados
- [x] Modelo LSTM treinado
- [x] Artefatos salvos (.keras, .joblib)
- [x] API FastAPI criada
- [x] Teste do endpoint /predict funcionando
- [ ] Documentação entregue (este README)
