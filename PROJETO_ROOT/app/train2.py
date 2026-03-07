import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import joblib

# 1. Carregar dataset enriquecido
try:
    df = pd.read_csv("features.csv")
    print("✅ Usando features.csv")
except FileNotFoundError:
    df = pd.read_csv("preprocessed.csv")
    print("⚠️ features.csv não encontrado, usando preprocessed.csv")

# 2. Separar X e y
drop_cols = [c for c in df.columns if c.startswith("Id") or "Observacao" in c]
X = df.drop(columns=drop_cols + ["Defasagem"], errors="ignore")
y = df["Defasagem"]

# 3. Divisão treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. Treinar modelo
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# 5. Avaliar modelo
y_pred = model.predict(X_test)
print("✅ Avaliação do modelo:")
print(classification_report(y_test, y_pred))
print("Matriz de confusão:")
print(confusion_matrix(y_test, y_pred))

# 6. Importância das features
importances = pd.Series(model.feature_importances_, index=X.columns)
top_features = importances.sort_values(ascending=False).head(10)
print("Top 10 features mais importantes:")
print(top_features)

# 7. Visualizar importância das features
plt.figure(figsize=(8,5))
top_features.plot(kind="bar")
plt.title("Top 10 Features mais importantes")
plt.ylabel("Importância")
plt.tight_layout()
plt.show()

# 8. Salvar modelo treinado
joblib.dump(model, "model.pkl")
print("💾 Modelo salvo em 'model.pkl'")