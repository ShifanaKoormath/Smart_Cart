import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import joblib
import pandas as pd

class ProductMLModel:
    def __init__(self, model_path="ml/knn_model.pkl"):
        self.model_path = model_path
        self.model = None

    def load(self):
        self.model = joblib.load(self.model_path)

    def predict(self, features):
        """
        features: dict with keys:
        weight, aspect_ratio, area_ratio, color_code
        """

        x = pd.DataFrame([{
            "weight": features["weight"],
            "aspect_ratio": features["aspect_ratio"],
            "area_ratio": features["area_ratio"],
            "color_code": features["color_code"]
        }])

        pred = self.model.predict(x)[0]
        probs = self.model.predict_proba(x)[0]

        confidence = max(probs)

        return pred, confidence