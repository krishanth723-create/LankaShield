import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# கோப்பு பாதைகளின் கட்டமைப்பு
BASE_DIR = Path(__file__).resolve().parent.parent
PREDICTIONS_PATH = BASE_DIR / 'data' / 'predictions_mock.csv'

def simulate_daily_predictions():
    # 1. இன்றைய தேதியைக் கண்டறிதல் (2026-06-09)
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    # 2. மாதிரித் தரவுகளின் அடிப்படை வடிவமைப்பு
    base_districts = [
        {"MOH_Division": "Galle Road (Colombo 04)", "latitude": 6.8966, "longitude": 79.8553},
        {"MOH_Division": "Wellawatte (Colombo 06)", "latitude": 6.8790, "longitude": 79.8610},
        {"MOH_Division": "Maradana Road (Colombo 10)", "latitude": 6.9245, "longitude": 79.8654},
        {"MOH_Division": "Negombo Road (Gampaha District)", "latitude": 7.2081, "longitude": 79.8426},
        {"MOH_Division": "Kadawatha Central (Gampaha District)", "latitude": 7.0012, "longitude": 79.9512},
        {"MOH_Division": "Galle Road (Kalutara District)", "latitude": 6.5851, "longitude": 79.9607}
    ]
    
    new_rows = []
    for dist in base_districts:
        # 3. மெஷின் லேர்னிங் மாடல் கணிப்பது போன்ற ஒரு உருவகப்படுத்துதல் (Simulation)
        # ஒவ்வொரு நாளும் வானிலைக்கு ஏற்ப எண்கள் மாறுபடும் (Randomized for demo)
        predicted_risk = np.random.randint(40, 98)
        sterile_release = int(predicted_risk * np.random.randint(500, 700))
        garbage_spots = np.random.randint(4, 22)
        
        new_rows.append({
            "date": today_str,
            "MOH_Division": dist["MOH_Division"],
            "latitude": dist["latitude"],
            "longitude": dist["longitude"],
            "Predicted_Risk_Score": predicted_risk,
            "Recommended_Sterile_Release": sterile_release,
            "Garbage_Spots": garbage_spots
        })
        
    new_df = pd.DataFrame(new_rows)
    
    # 4. புதிய தரவுகளைப் பழைய CSV கோப்பின் அடியில் சேர்த்தல் (Append to CSV)
    if os.path.exists(PREDICTIONS_PATH):
        old_df = pd.read_csv(PREDICTIONS_PATH)
        # ஏற்கனவே இன்றைய தேதி இருந்தால் மீண்டும் சேர்ப்பதைத் தவிர்க்கும் சரிபார்ப்பு
        if today_str in old_df['date'].astype(str).values:
            print(f"[{today_str}] தரவுகள் ஏற்கனவே CSV கோப்பில் உள்ளன.")
            return
        
        combined_df = pd.concat([old_df, new_df], ignore_index=True)
        combined_df.to_csv(PREDICTIONS_PATH, index=False)
        print(f"[{today_str}] புதிய தினசரி கணிப்புகள் வெற்றிகரமாக CSV கோப்பில் சேர்க்கப்பட்டன!")
    else:
        new_df.to_csv(PREDICTIONS_PATH, index=False)
        print("جد புதிய CSV கோப்பு உருவாக்கப்பட்டு தரவுகள் சேமிக்கப்பட்டன.")

if __name__ == "__main__":
    simulate_daily_predictions()
