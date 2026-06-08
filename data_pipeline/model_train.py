import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

load_dotenv()

# Load paths from .env
CASE_CSV_PATH = os.getenv("DENGUE_CASES_PATH")
WEATHER_LAG_FEATURES_PATH = os.getenv("WEATHER_LAG_FEATURES_PATH")
MODEL_PATH = os.getenv("MODEL_PATH", "./model/model.pkl")

if not CASE_CSV_PATH or not os.path.exists(CASE_CSV_PATH):
    raise FileNotFoundError("DENGUE_CASES_PATH not set or file does not exist.")
if not WEATHER_LAG_FEATURES_PATH or not os.path.exists(WEATHER_LAG_FEATURES_PATH):
    raise FileNotFoundError("WEATHER_LAG_FEATURES_PATH not set or file does not exist.")

# Load datasets
dengue_df = pd.read_csv(CASE_CSV_PATH, parse_dates=["date"])
weather_df = pd.read_csv(WEATHER_LAG_FEATURES_PATH, parse_dates=["date"])

# Merge on district and date (assuming both have these columns)
merged = pd.merge(dengue_df, weather_df, on=["district", "date"], how="inner")

# Target variable: cases (could also be binary hotspot flag)
Y = merged["cases"]
X = merged.drop(columns=["cases", "date", "district"]).fillna(0)

# Train‑test split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

model = GradientBoostingRegressor(random_state=42)
model.fit(X_train, y_train)

# Evaluation
preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)
print(f"Model MAE: {mae:.2f}")
print(f"Model R^2: {r2:.3f}")

# Ensure model directory exists
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(model, MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")
