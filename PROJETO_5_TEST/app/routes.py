import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

# Carregar um dataset de exemplo
X, y = load_iris(return_X_y=True)

# Treinar modelo
model = RandomForestClassifier()
model.fit(X, y)

# Salvar modelo em .pkl
joblib.dump(model, "random_forest_model.pkl")
print("Modelo salvo com sucesso!")