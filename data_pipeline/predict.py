import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import joblib
from datetime import datetime, timedelta

load_dotenv()

# Config paths
MODEL_PATH = os.getenv("MODEL_PATH", "./model/model.pkl")
WEATHER_LAG_FEATURES_PATH = os.getenv("WEATHER_LAG_FEATURES_PATH")
PREDICTIONS_PATH = os.getenv("PREDICTIONS_PATH", "./data/predictions.csv")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
if not WEATHER_LAG_FEATURES_PATH or not os.path.exists(WEATHER_LAG_FEATURES_PATH):
    raise FileNotFoundError("WEATHER_LAG_FEATURES_PATH not set or file does not exist.")

# Load model
model = joblib.load(MODEL_PATH)

# Load the most recent lagged weather features (assumes they are up‑to‑date)
weather_df = pd.read_csv(WEATHER_LAG_FEATURES_PATH, parse_dates=["date"])

# Prepare features for prediction – drop identifiers
X_pred = weather_df.drop(columns=["date", "district"]).fillna(0)

# Predict risk (case count) for each district/date in the weather dataframe
predictions = model.predict(X_pred)

result_df = weather_df[["district", "date"]].copy()
result_df["predicted_cases"] = predictions

# Ensure output directory exists
os.makedirs(os.path.dirname(PREDICTIONS_PATH), exist_ok=True)
result_df.to_csv(PREDICTIONS_PATH, index=False)
print(f"Predictions saved to {PREDICTIONS_PATH}")
