import pandas as pd
from src.preprocessing import load_all_data, create_target, preprocess


def test_load():
    # Carregar dados e mostrar colunas
    df = load_all_data()
    print("✅ Dados carregados")
    print("Colunas disponíveis:", df.columns.tolist()[:20])  # mostra só as primeiras 20
    print("Shape:", df.shape)
    return df

def test_target(df):
    # Criar variável alvo
    df = create_target(df)
    print("✅ Variável Defasagem criada")
    print("Distribuição da Defasagem:", df["Defasagem"].value_counts())
    return df

def test_preprocess(df):
    # Pré-processar
    df = preprocess(df)
    print("✅ Pré-processamento aplicado")
    print("Exemplo de linhas:")
    print(df.head())
    return df

if __name__ == "__main__":
    df = test_load()
    df = test_target(df)
    df = test_preprocess(df)