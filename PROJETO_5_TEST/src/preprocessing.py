import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

def load_all_data():
    # Carregar tabelas
    historico = pd.read_csv("doc/TbHistorico.csv")
    serie = pd.read_csv("data/TbSerie.csv")
    try:
        situacao_disciplina = pd.read_csv("data/TbSituacaoAlunoDisciplina.csv")
    except:
        situacao_disciplina = pd.DataFrame()

    # Carregar PEDE
    pede_2022 = pd.read_csv("data/pede2022.csv"); pede_2022["Ano"] = 2022
    pede_2023 = pd.read_csv("data/pede2023.csv"); pede_2023["Ano"] = 2023
    pede_2024 = pd.read_csv("data/pede2024.csv"); pede_2024["Ano"] = 2024
    pede = pd.concat([pede_2022, pede_2023, pede_2024], ignore_index=True)

    print("TbHistorico colunas:", historico.columns.tolist())
    print("TbSerie colunas:", serie.columns.tolist())
    if not situacao_disciplina.empty:
        print("TbSituacaoAlunoDisciplina colunas:", situacao_disciplina.columns.tolist())
    print("PEDE colunas:", pede.columns.tolist())

    # Merge inicial: histórico + série (pela coluna IdSerie_x do histórico)
    df = historico.copy()
    if "IdSerie_x" in df.columns and "IdSerie" in serie.columns:
        df = df.merge(serie, left_on="IdSerie_x", right_on="IdSerie", how="left")

    # Merge com PEDE (se tiver IdSerie)
    if "IdSerie_x" in df.columns and "IdSerie" in pede.columns:
        df = df.merge(pede, left_on="IdSerie_x", right_on="IdSerie", how="left")

    # Merge com situação disciplina (se tiver IdAluno)
    if not situacao_disciplina.empty and "IdAluno" in df.columns and "IdAluno" in situacao_disciplina.columns:
        df = df.merge(situacao_disciplina, on="IdAluno", how="left")

    return df

def create_target(df: pd.DataFrame):
    df["Defasagem"] = 0
    # Usa ResultadoFinal_x ou ResultadoFinal_y
    for col in ["ResultadoFinal_x", "ResultadoFinal_y"]:
        if col in df.columns:
            df.loc[df[col].isin(["R","Reprovado","Desistente"]), "Defasagem"] = 1
    return df

def preprocess(df: pd.DataFrame):
    numeric_cols = ["NotaFinal", "QuantidadeFaltasAnual"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col].fillna(df[col].mean(), inplace=True)

    categorical_cols = ["ResultadoFinal_x","ResultadoFinal_y","NomeSerie"]
    for col in categorical_cols:
        if col in df.columns:
            df[col].fillna("Desconhecido", inplace=True)
            df[col] = df[col].astype(str)
            df[col] = LabelEncoder().fit_transform(df[col])

    scaler = StandardScaler()
    for col in numeric_cols:
        if col in df.columns:
            df[col] = scaler.fit_transform(df[[col]])

    df.to_csv("preprocessed.csv", index=False)
    print(f"✅ Pré-processamento concluído! {df.shape[0]} linhas, {df.shape[1]} colunas.")
    return df

if __name__ == "__main__":
    df = load_all_data()
    df = create_target(df)
    df = preprocess(df)