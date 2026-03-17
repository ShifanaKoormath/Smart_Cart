# test_ml.py

from ml.model import ProductMLModel

ml_model = ProductMLModel()
ml_model.load()

# Example inputs (from your dataset patterns)
tests = [
    {"weight": 125, "aspect_ratio": 1.1, "area_ratio": 0.8, "color_code": 1},  # P001
    {"weight": 100, "aspect_ratio": 2.5, "area_ratio": 0.09, "color_code": 2}, # P004
    {"weight": 55, "aspect_ratio": 3.0, "area_ratio": 0.07, "color_code": 2},  # P005
    {"weight": 250, "aspect_ratio": 0.8, "area_ratio": 0.11, "color_code": 1}, # P007
]

for t in tests:
    pred, conf = ml_model.predict(t)
    print(f"Input: {t}")
    print(f"Prediction: {pred}, Confidence: {round(conf, 2)}\n")