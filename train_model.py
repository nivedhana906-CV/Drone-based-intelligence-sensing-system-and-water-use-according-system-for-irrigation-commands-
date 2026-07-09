"""
Trains a RandomForestClassifier on the Drone-based Intelligent ET
Sensing System dataset and saves the trained model, scaler,
and feature list for use by the Flask API.
"""

import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "dataset", "irrigation_data.csv")

FEATURES = [
    "Temperature",
    "Humidity",
    "SoilMoisture",
    "ET_Value",
    "Rainfall",
    "WindSpeed",
    "CropAge",
]

TARGET = "IrrigationRequired"

# Load Dataset
df = pd.read_csv(DATA_PATH)

X = df[FEATURES]
y = df[TARGET]

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Feature Scaling
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Random Forest Model
rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=6,
    random_state=42
)

rf.fit(X_train_scaled, y_train)

rf_pred = rf.predict(X_test_scaled)
rf_proba = rf.predict_proba(X_test_scaled)[:, 1]

print("===== Random Forest Model =====")
print("Accuracy :", accuracy_score(y_test, rf_pred))
print("ROC-AUC :", roc_auc_score(y_test, rf_proba))
print(classification_report(y_test, rf_pred))

# Logistic Regression
lr = LogisticRegression(max_iter=1000)

lr.fit(X_train_scaled, y_train)

lr_pred = lr.predict(X_test_scaled)

print("\n===== Logistic Regression =====")
print("Accuracy :", accuracy_score(y_test, lr_pred))

# Feature Importance
importances = dict(zip(FEATURES, rf.feature_importances_))

print("\nTop Influencing Features")

for feature, importance in sorted(importances.items(), key=lambda x: -x[1]):
    print(f"{feature}: {importance:.3f}")

# Save Model Files
with open(os.path.join(BASE_DIR, "model.pkl"), "wb") as f:
    pickle.dump(rf, f)

with open(os.path.join(BASE_DIR, "scaler.pkl"), "wb") as f:
    pickle.dump(scaler, f)

with open(os.path.join(BASE_DIR, "features.pkl"), "wb") as f:
    pickle.dump(FEATURES, f)

print("\nModel, scaler and feature list saved successfully.")
| Student Placement  | Un Drone Project    |
| ------------------ | ------------------- |
| placement_data.csv | irrigation_data.csv |
| CGPA               | Temperature         |
| SSC Marks          | Humidity            |
| HSC Marks          | Soil Moisture       |
| Internships        | ET_Value            |
| Projects           | Rainfall            |
| Certifications     | WindSpeed           |
| Aptitude Score     | CropAge             |
| Placed             | IrrigationRequired  |
