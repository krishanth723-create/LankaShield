# LankaShield

**Predicting Dengue Hotspots in Sri Lanka**

This repository contains three main components:

1. **Data pipeline** – fetches 14‑day lagged weather data, dengue case data, engineers features, trains a model, and generates risk predictions.
2. **Streamlit dashboard** – interactive web app that visualizes predicted risk zones on a map.
3. **React Native mobile app** – UI for health inspectors to view hotspots and confirm mosquito‑release actions.

## Project Structure
```
LankaShield/
├─ data_pipeline/      # Python data‑science pipeline
├─ dashboard/          # Streamlit web dashboard
└─ mobile/             # React Native inspector app
```

### Setup
```bash
# Clone repo (if remote) or navigate to the folder
cd "C:/Users/DELL/Desktop/LankaShield"

# ----- Data pipeline -----
python -m venv venv
venv\Scripts\activate
pip install -r data_pipeline/requirements.txt

# ----- Dashboard -----
cd dashboard
pip install -r requirements.txt
streamlit run app.py

# ----- Mobile app -----
cd ../mobile
npm install
npm start   # or "expo start" if using Expo
```

### License
MIT – feel free to adapt and improve.
