import pandas as pd

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria novas variáveis derivadas para enriquecer o dataset.
    """

    # 1. Taxa de faltas por carga horária
    if "QuantidadeFaltasAnual" in df.columns and "CargaHorariaAnual" in df.columns:
        df["TaxaFaltas"] = df["QuantidadeFaltasAnual"] / df["CargaHorariaAnual"]
        df["TaxaFaltas"].fillna(0, inplace=True)

    # 2. Média de notas por aluno
    if "NotaFinal" in df.columns and "IdAluno" in df.columns:
        df["MediaNotasAluno"] = df.groupby("IdAluno")["NotaFinal"].transform("mean")

    # 3. Histórico de reprovações acumuladas
    if "IdAluno" in df.columns and "ResultadoFinal_x" in df.columns:
        df["ReprovacoesAcumuladas"] = (
            df.groupby("IdAluno")["ResultadoFinal_x"]
              .transform(lambda x: (x.isin(["R","Reprovado","Desistente"])).cumsum())
        )

    # 4. Indicador de defasagem por série (se aluno repetiu série)
    if "IdAluno" in df.columns and "CodigoSerie_x" in df.columns:
        df["RepetiuSerie"] = (
            df.groupby("IdAluno")["CodigoSerie_x"].transform(lambda x: x.duplicated().astype(int))
        )

    # 5. Taxa de evasão aproximada (faltas / dias letivos)
    if "QuantidadeFaltasAnual" in df.columns and "DiasLetivos" in df.columns:
        df["TaxaEvasaoCalc"] = df["QuantidadeFaltasAnual"] / df["DiasLetivos"]
        df["TaxaEvasaoCalc"].fillna(0, inplace=True)

    return df

if __name__ == "__main__":
    df = pd.read_csv("preprocessed.csv")
    df = add_features(df)
    df.to_csv("features.csv", index=False)
    print(f"✅ Feature engineering concluído! {df.shape[0]} linhas, {df.shape[1]} colunas.")