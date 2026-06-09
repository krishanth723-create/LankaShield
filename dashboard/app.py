import os
import pandas as pd
import streamlit as st
try:
    from streamlit_folium import st_folium
except ImportError:
    st.error('streamlit_folium not installed. Please install dependencies.')
    st.stop()

try:
    import folium
except ImportError:
    st.error('folium not installed. Please install dependencies.')
    st.stop()
from pathlib import Path

# Project root directory configuration
BASE_DIR = Path(__file__).resolve().parent.parent
PREDICTIONS_PATH = str(BASE_DIR / 'data' / 'predictions_mock.csv')

# Configure clean widescreen framework parameters
st.set_page_config(layout="wide", page_title="LankaShield Dashboard")

st.title('🦟 LankaShield – Dengue Hotspot Prediction')

# Sidebar Controls Configuration
st.sidebar.header('Filters')
risk_threshold = st.sidebar.slider('Risk Score Threshold', min_value=0, max_value=100, value=50, step=5)
selected_date = st.sidebar.date_input('Prediction Date', value=pd.to_datetime('2026-06-08'))

# Data Loader Engine
@st.cache_data
def load_predictions(file_path):
    if not os.path.exists(file_path):
        st.error(f"Error: Data file not found at '{file_path}'. Please verify.")
        st.stop()
    try:
        df = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        st.error(f"Error processing CSV: {str(e)}")
        st.stop()

# Execution of data pipeline loader
pred_df = load_predictions(PREDICTIONS_PATH)

# Apply selected filters dynamically
filtered = pred_df[pred_df['date'] == pd.to_datetime(selected_date)]
filtered = filtered[filtered['Predicted_Risk_Score'] >= risk_threshold]

# Base map initialization centered over Western Province
m = folium.Map(location=[6.9000, 80.0000], zoom_start=9, tiles='CartoDB positron')

# Marker classification layout logic
def get_marker_color(score):
    if score >= 80: return 'red'
    elif score >= 50: return 'orange'
    else: return 'green'

# Inject markers into map canvas
if not filtered.empty:
    for _, row in filtered.iterrows():
        popup_template = f"""
        <div style="font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; width: 230px; line-height: 1.5; color: #333333;">
            <strong style="color: #1e293b; font-size: 14px; display: block; margin-bottom: 4px;">{row['MOH_Division']}</strong>
            <div style="border-top: 1px solid #e2e8f0; margin: 6px 0;"></div>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 2px 0; color: #64748b;">Dengue Threat Index:</td>
                    <td style="text-align: right; font-weight: bold; color: {'#ef4444' if row['Predicted_Risk_Score']>=80 else '#f97316' if row['Predicted_Risk_Score']>=50 else '#22c55e'};">{row['Predicted_Risk_Score']}%</td>
                </tr>
                <tr>
                    <td style="padding: 2px 0; color: #64748b;">Breeding Hotspots:</td>
                    <td style="text-align: right; font-weight: bold; color: #475569;">{int(row['Garbage_Spots'])} locations</td>
                </tr>
                <tr>
                    <td style="padding: 2px 0; color: #64748b;">Sterile Release Plan:</td>
                    <td style="text-align: right; font-weight: bold; color: #2563eb;">{int(row['Recommended_Sterile_Release']):,} units</td>
                </tr>
            </table>
        </div>
        """
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_template, max_width=260),
            icon=folium.Icon(color=get_marker_color(row['Predicted_Risk_Score']), icon='info-sign')
        ).add_to(m)

# ==============================================================================
# 🌟 DYNAMIC FLEXBOX METRIC MESH INTERFACE COMPONENT
# ==============================================================================

st.subheader('📊 Localized Surveillance Command Center')
st.caption('Real-time biometric threat classifications across monitored Western Province zones:')

if not filtered.empty:
    # Create rows of three columns
    for i, (_, row) in enumerate(filtered.iterrows()):
        if i % 3 == 0:
            cols = st.columns(3)
        col = cols[i % 3]
        with col:
            with st.container():
                st.subheader(row['MOH_Division'])
                score = row['Predicted_Risk_Score']
                if score >= 80:
                    label = "🚨 CRITICAL"
                elif score >= 50:
                    label = "⚠️ ELEVATED"
                else:
                    label = "✅ CONTROLLED"
                st.metric(label=label, value=f"{score}%")
                units = int(row['Recommended_Sterile_Release'])
                garbage = int(row['Garbage_Spots'])
                st.caption(f"📦 Sterile Release Plan: {units:,} units | 🗑️ {garbage} Waste Hotspots")
else:
    st.info("No active surveillance networks match the current filtering criteria.")

# Show raw table layout matrix
st.subheader('Filtered Predictions Data Matrix')
st.dataframe(filtered)

# Deploy interactive workspace rendering canvas using a fresh compilation key
st_folium(m, width=1200, height=600, key="western_province_mesh_v12_production_final")

st.write('---')
st.caption('Data source: dengue case reports and 14‑day localized predictive analysis engine.')








