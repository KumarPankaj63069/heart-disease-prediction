import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
import pickle

# ================= LOAD DATA =================
data = pd.read_csv("heart.csv")

# Features & Target
X = data.drop("target", axis=1)
y = data["target"]

# ================= HANDLE IMBALANCE =================
smote = SMOTE(random_state=42)
X_res, y_res = smote.fit_resample(X, y)

# ================= SPLIT =================
X_train, X_test, y_train, y_test = train_test_split(
    X_res, y_res, test_size=0.2, random_state=42
)

# ================= MODELS =================
models = {
    "Logistic Regression": LogisticRegression(max_iter=2000),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
}

best_model = None
best_accuracy = 0

print("Training Models...\n")

for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    acc = accuracy_score(y_test, predictions)
    print(f"{name} Accuracy: {acc:.4f}")

    if acc > best_accuracy:
        best_accuracy = acc
        best_model = model

# ================= SAVE MODEL =================
pickle.dump(best_model, open("model.pkl", "wb"))

# ================= SAVE FEATURE ORDER =================
pickle.dump(X.columns.tolist(), open("features.pkl", "wb"))

print("\n✅ Best Model Saved Successfully!")
print("Best Accuracy:", best_accuracy)