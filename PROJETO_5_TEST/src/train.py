import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# 1. Carregar dataset pré-processado
df = pd.read_csv("preprocessed.csv")

# 2. Remover colunas não úteis
df = df.drop(columns=["RA", "Nome", "Destaque IEG", "Destaque IDA", "Destaque IPV"])

# 3. Codificar colunas categóricas
categorical_cols = df.select_dtypes(include=["object"]).columns
encoder = LabelEncoder()
for col in categorical_cols:
    df[col] = encoder.fit_transform(df[col])

# 4. Features e target
X = df.drop(columns=["Indicado"])
y = df["Indicado"]

# 5. Divisão treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 6. Definir modelo base
rf = RandomForestClassifier(random_state=42, class_weight="balanced")

# 7. Definir grid de hiperparâmetros
param_grid = {
    "n_estimators": [100, 200, 300],
    "max_depth": [5, 10, 15, None],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4]
}

# 8. Rodar GridSearchCV
grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=5,
    n_jobs=1,    # força execução em um único processo
    scoring="f1_macro"
)
grid_search.fit(X_train, y_train)

print("Melhores parâmetros encontrados:", grid_search.best_params_)

# 9. Avaliar modelo final
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

print("Acurácia:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# 10. Importância das variáveis
importances = best_model.feature_importances_
features = X.columns

plt.figure(figsize=(10,6))
plt.barh(features, importances)
plt.xlabel("Importância")
plt.ylabel("Variáveis")
plt.title("Importância das Features - Random Forest (GridSearch)")
plt.tight_layout()
plt.savefig("feature_importance.png")  # salva gráfico em PNG
plt.show()

import joblib
joblib.dump(best_model, "random_forest_model.pkl")
print("Modelo salvo em random_forest_model.pkl")