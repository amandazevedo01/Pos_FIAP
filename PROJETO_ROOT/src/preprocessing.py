import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

def load_all_data():
    # Carregar tabelas principais
    historico = pd.read_csv("data/TbHistorico.csv")
    serie = pd.read_csv("data/TbSerie.csv")

    # Carregar PEDE
    pede_2022 = pd.read_csv("data/pede2022.csv"); pede_2022["Ano"] = 2022
    pede_2023 = pd.read_csv("data/pede2023.csv"); pede_2023["Ano"] = 2023
    pede_2024 = pd.read_csv("data/pede2024.csv"); pede_2024["Ano"] = 2024
    pede = pd.concat([pede_2022, pede_2023, pede_2024], ignore_index=True)

    # Merge inicial
    df = historico.copy()
    if "IdSerie_x" in df.columns and "IdSerie" in serie.columns:
        df = df.merge(serie, left_on="IdSerie_x", right_on="IdSerie", how="left")
    if "IdSerie_x" in df.columns and "IdSerie" in pede.columns:
        df = df.merge(pede, left_on="IdSerie_x", right_on="IdSerie", how="left")

    return df

def create_target(df: pd.DataFrame):
    df["Defasagem"] = 0
    for col in ["ResultadoFinal_x", "ResultadoFinal_y"]:
        if col in df.columns:
            df.loc[df[col].isin(["R","Reprovado","Desistente"]), "Defasagem"] = 1
    return df

def preprocess(df: pd.DataFrame):
    # Colunas numéricas reais
    numeric_cols = ["NotaFinal", "QuantidadeFaltasAnual", "IDEB", "TaxaEvasao", "TaxaReprovacao"]
    for col in numeric_cols:
        if col in df.columns:
            # Converter para número, forçando strings inválidas para NaN
            df[col] = pd.to_numeric(df[col], errors="coerce")
            # Preencher NaN com média
            df[col].fillna(df[col].mean(), inplace=True)

    # Colunas categóricas (inclui códigos de série e resultado final)
    categorical_cols = ["CodigoSerie_x","CodigoSerie_y","NomeSerie",
                        "ResultadoFinal_x","ResultadoFinal_y",
                        "SituacaoAlunoTurma","SituacaoAlunoDisciplina",
                        "Descricao","TurnoPrincipal","TipoResponsavel"]
    for col in categorical_cols:
        if col in df.columns:
            df[col].fillna("Desconhecido", inplace=True)
            df[col] = df[col].astype(str)
            df[col] = LabelEncoder().fit_transform(df[col])

    # Normalizar numéricos
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