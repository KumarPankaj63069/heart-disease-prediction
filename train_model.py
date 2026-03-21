import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
import pickle

# ================= LOAD DATA =================
data = pd.read_csv("heart.csv")

X = data.drop("target", axis=1)
y = data["target"]

# ================= SPLIT FIRST =================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ================= APPLY SMOTE ONLY ON TRAIN =================
smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

# ================= MODEL =================
model = LogisticRegression(max_iter=2000)

print("Training Model...\n")

model.fit(X_train, y_train)

# ================= TEST =================
predictions = model.predict(X_test)

acc = accuracy_score(y_test, predictions)
print("Accuracy:", acc)

# ================= SAVE =================
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(X.columns.tolist(), open("features.pkl", "wb"))

print("\n✅ Model Saved Successfully!")