import pandas as pd
import numpy as np

def load_weather(csv_path: str) -> pd.DataFrame:
    """Load raw weather CSV with columns: date, district, temp, precipitation, humidity, etc."""
    df = pd.read_csv(csv_path, parse_dates=["date"])
    return df

def create_lag_features(df: pd.DataFrame, lag_days: int = 14) -> pd.DataFrame:
    """Create lag aggregations (mean, max, min) for each numeric weather variable.
    Returns a DataFrame indexed by district and date with lag feature columns.
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    # Exclude any identifier columns if present
    id_cols = [c for c in ["date", "district"] if c in df.columns]
    feature_frames = []
    for col in numeric_cols:
        for agg in ["mean", "max", "min"]:
            lag_name = f"{col}_{agg}_{lag_days}d"
            rolled = (
                df.set_index(["district", "date"])\
                  .groupby(level=0)[col]
                  .rolling(window=lag_days, min_periods=1)
                  .agg(agg)
                  .reset_index(name=lag_name)
            )
            feature_frames.append(rolled)
    # Merge all features on district & date
    features = feature_frames[0]
    for frame in feature_frames[1:]:
        features = features.merge(frame, on=["district", "date"], how="left")
    return features

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python feature_engineering.py <weather_csv_path>")
        sys.exit(1)
    weather_path = sys.argv[1]
    df = load_weather(weather_path)
    lag_df = create_lag_features(df)
    lag_df.to_csv("weather_lag_features.csv", index=False)
    print("Lag features saved to weather_lag_features.csv")
