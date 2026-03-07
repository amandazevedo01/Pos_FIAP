import pandas as pd
from sklearn.preprocessing import LabelEncoder

def test_label_encoding():
    df = pd.DataFrame({"col": ["A", "B", "A", "C"]})
    encoder = LabelEncoder()
    df["col_encoded"] = encoder.fit_transform(df["col"])
    
    # Verifica se o número de categorias bate
    assert len(set(df["col_encoded"])) == 3
    # Verifica se não há valores nulos
    assert df["col_encoded"].isnull().sum() == 0