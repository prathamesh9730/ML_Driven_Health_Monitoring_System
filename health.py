import pickle
import numpy as np

# Load trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_status(data):
    """
    data = list/array of sensor values [hr, spo2, temp, ...]
    returns: Normal / Warning / Critical
    """
    data = np.array(data).reshape(1, -1)
    prediction = model.predict(data)[0]
    return prediction
