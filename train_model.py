import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pickle

# Load data
data = pd.read_csv("heart.csv")

# 🔥 ONLY FORM FEATURES
features = ["age", "sex", "cp", "trestbps", "chol", "fbs", "thalach", "exang"]

X = data[features]
y = data["target"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Model
model = Pipeline([
    ("scaler", StandardScaler()),
    ("lr", LogisticRegression(max_iter=2000))
])

model.fit(X_train, y_train)

# Save
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(features, open("features.pkl", "wb"))

print("✅ MODEL TRAINED WITH CORRECT FEATURES")