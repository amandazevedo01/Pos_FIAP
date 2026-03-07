import joblib
import numpy as np

def test_model_load_and_predict():
    model = joblib.load("random_forest_model.pkl")
    
    # Cria um exemplo fictício com o mesmo número de features
    X_fake = np.random.rand(1, model.n_features_in_)
    
    pred = model.predict(X_fake)
    
    # Verifica se retorna uma previsão válida (0 ou 1)
    assert pred[0] in [0, 1]