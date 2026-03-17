import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib

# -------- Load dataset --------
df = pd.read_csv("ml/dataset.csv")

X = df[["weight", "aspect_ratio", "area_ratio", "color_code"]]
y = df["product_id"]

# -------- Split data --------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -------- Train model --------
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

# -------- Predict --------
y_pred = model.predict(X_test)

# -------- Classification Report --------
print("\n=== Classification Report ===\n")
print(classification_report(y_test, y_pred))

# -------- Confusion Matrix --------
labels = sorted(y.unique())

cm = confusion_matrix(y_test, y_pred, labels=labels)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)

fig, ax = plt.subplots(figsize=(8, 6))
disp.plot(ax=ax, cmap="Blues", values_format="d")

plt.title("Confusion Matrix (Smart Cart ML)")
plt.xticks(rotation=45)
plt.tight_layout()

# -------- Save image --------
plt.savefig("ml/confusion_matrix.png")
print("\nConfusion matrix saved to ml/confusion_matrix.png")

# -------- Optional: Save model again --------
joblib.dump(model, "ml/knn_model.pkl")