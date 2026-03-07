import pandas as pd
from sklearn.preprocessing import LabelEncoder

def encode_categorical(df: pd.DataFrame, categorical_cols: list) -> pd.DataFrame:
    """Transforma variáveis categóricas em numéricas."""
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
    return df