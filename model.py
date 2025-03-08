import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.combine import SMOTETomek
from xgboost import XGBClassifier
import pickle
import streamlit as st

# Load dataset
df = pd.read_csv("Crop_recommendationV2 (1).csv")

# Encode target variable (label)
le = LabelEncoder()
df['label'] = le.fit_transform(df['label'])

# Select 10 most relevant features
selected_features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'soil_moisture', 'soil_type', 'sunlight_exposure']
X = df[selected_features]
y = df['label']

# Feature Scaling
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Handle class imbalance using SMOTETomek
smote_tomek = SMOTETomek(random_state=42)
X_train, y_train = smote_tomek.fit_resample(X_train, y_train)

# Hyperparameter tuning using RandomizedSearchCV
param_grid = {
    'n_estimators': [100, 200],
    'learning_rate': [0.1],
    'max_depth': [6, 10]
}

random_search = RandomizedSearchCV(XGBClassifier(random_state=42), param_distributions=param_grid, cv=3, n_iter=5, scoring='accuracy', n_jobs=-1, random_state=42)
random_search.fit(X_train, y_train)

# Train best XGBoost model
best_params = random_search.best_params_
model = XGBClassifier(**best_params, random_state=42)
model.fit(X_train, y_train)

# Save the model
with open("crop_prediction_model.pkl", "wb") as file:
    pickle.dump((model, le, scaler), file)

print("Model training completed with optimized XGBoost and saved as 'crop_prediction_model.pkl'")
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy:.2f}")
