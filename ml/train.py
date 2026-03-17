import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load dataset
df = pd.read_csv("ml/dataset.csv")

# Features + label
X = df[["weight", "aspect_ratio", "area_ratio", "color_code"]]
y = df["product_id"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)

print("\n=== Classification Report ===\n")
print(classification_report(y_test, y_pred))

# Save
joblib.dump(model, "ml/knn_model.pkl")

print("\nModel saved to ml/knn_model.pkl")