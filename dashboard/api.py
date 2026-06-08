from fastapi import FastAPI
import pandas as pd

app = FastAPI(title="LankaShield API Portal 🇱🇰")

# டேஷ்போர்டில் இருக்கும் அதே மாதிரி தரவு
MOCK_DATA = {
    'id': ['1', '2', '3', '4'],
    'MOH_Division': ['Colombo Municipal', 'Dehiwala', 'Gampaha', 'Kaduwela'],
    'latitude': [6.9271, 6.8483, 7.0873, 6.9244],
    'longitude': [79.8612, 79.8778, 79.9925, 80.0004],
    'Predicted_Risk_Score': [85, 72, 90, 65],
    'Recommended_Sterile_Release': [50000, 35000, 60000, 30000],
    'status': ['Pending', 'Pending', 'Pending', 'Pending']
}

df = pd.DataFrame(MOCK_DATA)

# மொபைல் ஆப் தரவுகளைப் பெறுவதற்கான API Endpoint
@app.get("/api/v1/hotspots")
def get_mobile_hotspots():
    # டேட்டாவை மொபைல் ஆப்பிற்கு புரியும் JSON வடிவிற்கு மாற்றுதல்
    return df.to_dict(orient="records")

# PHI அதிகாரி கொசுக்களைத் திறந்துவிட்டதும் மொபைலில் இருந்து அப்டேட் செய்ய
@app.post("/api/v1/release/{item_id}")
def confirm_release(item_id: str):
    if item_id in df['id'].values:
        # நிலையை 'Completed' என மாற்றுதல்
        return {"status": "success", "message": f"Release confirmed for Hub {item_id}"}
    return {"status": "error", "message": "Invalid Hub ID"}
