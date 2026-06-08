import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/onecall/timemachine"


def fetch_weather(lat: float, lon: float, date: datetime) -> pd.DataFrame:
    """Fetch historical weather for a single day (24‑hour period) at given coordinates.
    Returns a DataFrame with hourly temperature, humidity, precipitation, etc.
    """
    timestamp = int(date.timestamp())
    params = {
        "lat": lat,
        "lon": lon,
        "dt": timestamp,
        "appid": API_KEY,
        "units": "metric",
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    hourly = data.get("hourly", [])
    records = []
    for hour in hourly:
        records.append({
            "datetime": datetime.fromtimestamp(hour["dt"]),
            "temp": hour.get("temp"),
            "humidity": hour.get("humidity"),
            "precip": hour.get("rain", {}).get("1h", 0),
        })
    return pd.DataFrame(records)


def fetch_bulk_weather(locations: list[tuple[float, float]], start_date: datetime, days: int = 14) -> pd.DataFrame:
    """Fetch weather for multiple locations over a range of days.
    Returns a concatenated DataFrame with columns: lat, lon, datetime, temp, humidity, precip.
    """
    all_frames = []
    for lat, lon in locations:
        for offset in range(days):
            date = start_date - timedelta(days=offset)
            df = fetch_weather(lat, lon, date)
            df["lat"] = lat
            df["lon"] = lon
            all_frames.append(df)
    return pd.concat(all_frames, ignore_index=True)
