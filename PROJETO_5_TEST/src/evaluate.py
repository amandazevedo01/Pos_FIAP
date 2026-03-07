import pandas as pd
import joblib
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

# 1. Carregar dataset pré-processado
df = pd.read_csv("preprocessed.csv")
df = df.drop(columns=["RA", "Nome", "Destaque IEG", "Destaque IDA", "Destaque IPV"])

# 2. Codificar colunas categóricas
categorical_cols = df.select_dtypes(include=["object"]).columns
encoder = LabelEncoder()
for col in categorical_cols:
    df[col] = encoder.fit_transform(df[col])

# 3. Features e target
X = df.drop(columns=["Indicado"])
y = df["Indicado"]

# 4. Carregar modelo salvo
model = joblib.load("random_forest_model.pkl")

# 5. Fazer previsões
y_pred = model.predict(X)

# 6. Avaliar desempenho
print("Acurácia:", accuracy_score(y, y_pred))
print(classification_report(y, y_pred))