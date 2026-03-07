from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate_model(model, X_test, y_test, threshold=0.3):
    """
    Avalia o modelo com várias métricas e retorna relatório.
    """
    # Probabilidades
    y_pred_proba = model.predict_proba(X_test)[:,1]
    # Classificação binária com threshold customizado
    y_pred = (y_pred_proba >= threshold).astype(int)

    # Métricas principais
    report = classification_report(y_test, y_pred, digits=3)
    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred_proba)
    cm = confusion_matrix(y_test, y_pred)

    print("=== Classification Report ===")
    print(report)
    print(f"Accuracy: {acc:.3f}")
    print(f"ROC AUC: {auc:.3f}")
    print("=== Confusion Matrix ===")
    print(cm)

    # Opcional: plotar matriz de confusão
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Predito")
    plt.ylabel("Real")
    plt.title("Matriz de Confusão")
    plt.show()

    return {
        "report": report,
        "accuracy": acc,
        "roc_auc": auc,
        "confusion_matrix": cm.tolist()
    }