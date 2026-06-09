# LankaShield

LankaShield is an interactive **Streamlit** dashboard that visualises dengue hotspot predictions across the Western Province, Sri Lanka. It combines real‑time risk scores, breeding hotspot locations, and sterile‑male release plans on a **Folium** map with rich, dynamic pop‑ups.

## ✨ Key Features
- **Automated Daily Pipeline (`predict.py`):** A background module that automatically simulates climate variance and appends fresh predictive indices to the local ledger every day.
- **Live Daily Pipeline & Filtration (`app.py`):** Real-time data parsing decoupled from static dates. Strategic planners can filter historical ranges via the sidebar to extract exact metrics for the selected day.
- **Dynamic Risk Scoring:** Integrated risk‑threshold slider to dynamically isolate high-threat zones.
- **Responsive Folium Map:** Coloured markers mapping threat indices (`red` ≥ 80, `orange` ≥ 50, `green` < 50) over a clean canvas layer.
- **Rich HTML Popups:** Modern UI popups displaying division metrics, custom fonts, and real-time biometric threat colors.
- **Metrics Summary Mesh:** Displays real-time biometric classifications utilizing a clear three‑column structural layout.

## 🏗️ Project Architecture & File Structure

```text
LankaShield/
│
├── dashboard/
│   ├── app.py                # Updated Live Streamlit Web Dashboard Application
│   ├── predict.py            # Automated Daily Predictive Simulation Pipeline
│   └── data/
│       └── predictions_mock.csv # Secure data ledger holding daily simulated records
│
├── README.md                 # Updated Project Documentation
└── requirements.txt          # Required Python dependencies
```

## 📦 Installation & Setup
```bash
# Clone the repository
git clone https://github.com
cd LankaShield

# Install required packages
python -m pip install -r requirements.txt
```
> The `requirements.txt` includes: `streamlit`, `streamlit-folium`, `folium`, `pandas`, `numpy`, `xgboost`, `scikit-learn`.

## 🚀 Running the Dashboard

### 1. Execute the Automated Prediction Pipeline
Before booting the interface dashboard, run the automation module to append the current date records to your secure ledger array:
```bash
cd dashboard
python predict.py
```

### 2. Run the Streamlit Live Dashboard
Launch the interface locally via your standard loopback module:
```bash
python -m streamlit run app.py
```
Open the displayed URL (usually <http://localhost:8501>) in your browser.

## 📊 Data Analytics Pipeline
- **Predictions CSV (`predictions_mock.csv`)** – Secure data ledger containing multi-platform metrics: `date`, `MOH_Division`, `latitude`, `longitude`, `Predicted_Risk_Score`, `Recommended_Sterile_Release`, `Garbage_Spots`.
- **Feature Engineering:** Employs historical weather variance metrics shifted by a 14-day delay pattern to accurately track the *Aedes* mosquito lifecycle.

## 📖 License
This project is licensed under the **MIT License**.

---
*Happy mapping and stay safe from dengue!*

