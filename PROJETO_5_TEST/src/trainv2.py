import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

# 1. Carregar dataset pré-processado
df = pd.read_csv("preprocessed.csv")

# 2. Remover colunas não úteis (identificadores e textos descritivos)
df = df.drop(columns=["RA", "Nome", "Destaque IEG", "Destaque IDA", "Destaque IPV"])

# 3. Codificar colunas categóricas restantes
categorical_cols = df.select_dtypes(include=["object"]).columns
encoder = LabelEncoder()
for col in categorical_cols:
    df[col] = encoder.fit_transform(df[col])

# 4. Definir features (X) e target (y)
X = df.drop(columns=["Indicado"])
y = df["Indicado"]

# 5. Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 6. Definir modelos para comparação
models = {
    "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "SVM": SVC(kernel="linear", random_state=42)
}

# 7. Treinar e avaliar cada modelo
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"\n=== {name} ===")
    print("Acurácia:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    # Validação cruzada para estabilidade
    scores = cross_val_score(model, X, y, cv=5)
    print("Cross-val média:", scores.mean())