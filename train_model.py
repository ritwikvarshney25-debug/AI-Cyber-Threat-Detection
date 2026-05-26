import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
data = pd.read_csv("dataset/data.csv", header=None)

# Features and labels
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Encode all categorical columns
for col in X.columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))

# Encode target labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y.astype(str))

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=50)

model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)

# Save model

import os

os.makedirs("model", exist_ok=True)

joblib.dump(
    model,
    "model/trained_model.pkl"
)

print("Model Saved Successfully")