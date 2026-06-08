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

# Load environment variables (if .env exists)
from dotenv import load_dotenv
load_dotenv()

# Paths
PREDICTIONS_PATH = os.getenv('PREDICTIONS_PATH', 'data/predictions.csv')
GEOMETRY_PATH = os.getenv('GEOMETRY_PATH', 'data/districts.geojson')

st.title('🦟 LankaShield – Dengue Hotspot Prediction')

# Logo
st.image('C:/Users/DELL/.gemini/antigravity-ide/brain/cf1cf93e-1980-459e-a335-04f1d67209db/lankashield_logo_1780894058203.png', width=200)

# Sidebar controls
st.sidebar.header('Filters')
# Risk score threshold slider
risk_threshold = st.sidebar.slider('Risk Score Threshold', min_value=0, max_value=100, value=50, step=5)
selected_date = st.sidebar.date_input('Prediction Date', value=pd.to_datetime('today'))

# Load predictions
@st.cache_data

@st.cache_data
def load_predictions():
    data = {
        'date': ['2026-06-08', '2026-06-08', '2026-06-08', '2026-06-08', '2026-06-08'],
        'MOH_Division': ['Colombo Municipal', 'Dehiwala', 'Gampaha', 'Negombo', 'Kaduwela'],
        'latitude': [6.9271, 6.8483, 7.0873, 7.2081, 6.9244],
        'longitude': [79.8612, 79.8778, 79.9925, 79.8426, 80.0004],
        'Predicted_Risk_Score': [85, 72, 90, 45, 65],
        'Recommended_Sterile_Release': [50000, 35000, 60000, 15000, 30000]
    }
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df


# வரைபடத்தை உருவாக்குதல் (இலங்கையை மையமாகக் கொண்டு)
pred_df = load_predictions()
# Apply date filter and risk threshold
filtered = pred_df[pred_df['date'] == pd.to_datetime(selected_date)]
filtered = filtered[filtered['Predicted_Risk_Score'] >= risk_threshold]

# Create map
m = folium.Map(location=[7.8731, 80.7718], zoom_start=7, tiles='CartoDB positron')

# Add markers for each prediction
for _, row in filtered.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=8,
        popup=(f"{row['MOH_Division']}: {row['Predicted_Risk_Score']}"),
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6
    ).add_to(m)

risk_dict = dict(zip(filtered['MOH_Division'], filtered['Predicted_Risk_Score']))

# Display metrics for each district
st.subheader('Risk Scores by District')
cols = st.columns(len(risk_dict))
for (district, score), col in zip(risk_dict.items(), cols):
    col.metric(label=district, value=str(score))

# Show filtered predictions table
st.subheader('Filtered Predictions')
st.dataframe(filtered)

# choropleth and geojson sections commented out pending data
# folium.Choropleth(
#     geo_data=geojson,
#     name='choropleth',
#     data=filtered,
#     columns=['MOH_Division', 'Predicted_Risk_Score'],
#     key_on='feature.properties.name',
#     fill_color='YlOrRd',
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name='Predicted Risk Score (higher = higher risk)',
# ).add_to(m)
#
# # Add tooltip for each district
# style_function = lambda x: {'fillColor': '#ffffff', 'color':'#000000','fillOpacity':0,'weight':0.1}
# highlight_function = lambda x: {'fillColor': '#000000', 'color':'#000000','fillOpacity':0.50,'weight':0.1}
# folium.GeoJson(
#     geojson,
#     style_function=style_function,
#     highlight_function=highlight_function,
#     tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['District:'], localize=True)
# ).add_to(m)

st_folium(m, width=1200, height=800)

st.write('---')
st.caption('Data source: dengue case reports and 14‑day lagged weather variables.')
