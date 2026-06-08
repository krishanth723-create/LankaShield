# LankaShield

![LankaShield Logo](https://raw.githubusercontent.com/your-repo/LankaShield/main/lankashield_logo.png)

## 🎯 Project Overview
LankaShield is an interactive **Streamlit** dashboard that visualises dengue hotspot predictions across Colombo, Sri Lanka. It combines real‑time risk scores, breeding hotspot locations, and sterile‑male release plans on a **Folium** map with rich, dynamic pop‑ups.

> **New Feature:** The map now uses a custom `folium.Marker` loop with a styled HTML popup (see `dashboard/app.py`). The popup displays:
> - Division name
> - Dengue Threat Index (color‑coded by risk)
> - Number of breeding hotspots
> - Recommended sterile release units

## ✨ Key Features
- **Dynamic risk scoring** with a risk‑threshold slider.
- **Date filter** to view predictions for a specific day.
- **Responsive Folium map** with coloured markers (`red` ≥ 80, `orange` ≥ 50, `green` < 50).
- **Rich HTML popups** – modern UI with custom fonts, colours, and layout.
- **Metrics summary** displayed in a three‑column layout.
- **Data table** for detailed view of filtered predictions.

## 📦 Installation
```bash
# Clone the repository
git clone https://github.com/your-repo/LankaShield.git
cd LankaShield

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```
> The `requirements.txt` includes:
> - `streamlit`
> - `streamlit-folium`
> - `folium`
> - `pandas`
> - `python-dotenv`

## 🚀 Running the Dashboard
```bash
streamlit run dashboard/app.py
```
Open the displayed URL (usually <http://localhost:8501>) in your browser.

## 🛠️ Configuration
Create a `.env` file in the project root to override default data paths:
```dotenv
PREDICTIONS_PATH=data/predictions.csv
GEOMETRY_PATH=data/districts.geojson
```
If omitted, the defaults defined in `app.py` are used.

## 📊 Data Sources
- **Predictions CSV** – synthetic data with columns: `date`, `MOH_Division`, `latitude`, `longitude`, `Predicted_Risk_Score`, `Recommended_Sterile_Release`, `Garbage_Spots`.
- **GeoJSON** – optional district boundaries (not currently rendered).

## 🎨 Styling Notes
The new popup HTML uses:
- **Segoe UI** font family for a clean, modern look.
- **Dynamic colour coding** for risk levels (`#ef4444`, `#f97316`, `#22c55e`).
- **Responsive layout** fitting within a 230 px width.

## 📖 License
This project is licensed under the **MIT License**.

---
*Happy mapping and stay safe from dengue!*
