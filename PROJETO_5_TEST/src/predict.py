import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# 1. Carregar dados
df = pd.read_csv("preprocessed.csv")

# 2. Remover colunas não úteis
df = df.drop(columns=["RA", "Nome", "Destaque IEG", "Destaque IDA", "Destaque IPV"], errors="ignore")

# 3. Codificar colunas categóricas
categorical_cols = df.select_dtypes(include=["object"]).columns
encoder = LabelEncoder()
for col in categorical_cols:
    df[col] = encoder.fit_transform(df[col])

# 4. Separar features (sem a coluna alvo)
X = df.drop(columns=["Indicado"], errors="ignore")

# 5. Carregar modelo salvo
model = joblib.load("random_forest_model.pkl")

# 6. Fazer previsões
predicoes = model.predict(X)
probas = model.predict_proba(X)

# 7. Adicionar colunas de previsão e probabilidade
df["Previsto"] = predicoes
df["Probabilidade_Indicado"] = probas[:, 1]  # segunda coluna = classe 1

# 8. Salvar resultados
df.to_csv("predicoes.csv", index=False)
print("Previsões e probabilidades salvas em predicoes.csv")