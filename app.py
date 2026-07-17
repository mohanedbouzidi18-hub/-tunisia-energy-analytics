import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import random
import requests

st.set_page_config(page_title="Tunisia Energy Pro", page_icon="⚡", layout="wide")
st.markdown("""<style>.stApp { background: linear-gradient(135deg, #1a0a2e, #0b0e14); color: white; }
    h1 { color: #58a6ff !important; text-align: center; font-weight: 900; }</style>""", unsafe_allow_html=True)
if 'history' not in st.session_state: st.session_state.history = []
API_KEY = "abcdea1d329150e0d98cee0fd38c3576"
def get_live_temp(region):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={region},TN&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url).json()
        return response['main']['temp']
    except:
        return 30.0
def calculate_risk(temp, hour, region):
    region_weights = {'Tunis': 0.15, 'Sousse': 0.12, 'Mahdia': 0.08, 'Sidi Bou Zid': 0.05, 'Sfax': 0.10}
    heat_impact = (temp - 20) * 0.02
    peak_impact = 0.3 if 14 <= hour <= 18 else 0
    return min(max(region_weights.get(region, 0.05) + heat_impact + peak_impact + random.uniform(-0.02, 0.02), 0.05), 0.95)
st.markdown("<h1>⚡ TUNISIA ENERGY ANALYTICS ⚡</h1>", unsafe_allow_html=True)
region = st.selectbox("🌍 اختر المنطقة:", ['Tunis', 'Sousse', 'Mahdia', 'Sidi Bou Zid', 'Sfax'])
live_temp = get_live_temp(region)
c1, c2 = st.columns(2)
temp = c1.slider("🌡️ الحرارة (°C):", 20, 50, float(live_temp))
hour = c2.number_input("⏰ الساعة:", 0, 23, value=datetime.now().hour)
p_val = calculate_risk(temp, hour, region)
b_color = "#ff4b4b" if p_val > 0.7 else ("#ffa500" if p_val > 0.4 else "#58a6ff")
st.markdown(f"""<div style="width: 100%; height: 20px; background: #333; border-radius: 10px;">
    <div style="width: {p_val*100}%; height: 100%; background: {b_color}; border-radius: 10px;"></div></div>""", unsafe_allow_html=True)
if st.button("🚀 تشغيل التنبؤ"):
    st.session_state.history.append({"الوقت": datetime.now().strftime("%H:%M"), "المنطقة": region, "الخطر": f"{p_val:.2%}"})
    st.success(f"تم تسجيل التنبؤ: {p_val:.2%}")
col_a, col_b = st.columns([2, 1])
with col_a:
    df_area = pd.DataFrame({'T': np.linspace(20, 50, 20), 'R': [calculate_risk(t, hour, region) for t in np.linspace(20, 50, 20)]})
    st.plotly_chart(px.area(df_area, x='T', y='R', template="plotly_dark"), use_container_width=True)
with col_b:
    st.plotly_chart(px.pie(values=[p_val, 1-p_val], names=['Risk', 'Stable'], hole=0.7), use_container_width=True)
st.subheader("📜 سجل التنبؤات")
st.dataframe(pd.DataFrame(st.session_state.history).tail(5), use_container_width=True)
st.markdown("💡 **تحليل:** يتم الاعتماد على بيانات الطقس الحية ونماذج التنبؤ بالأحمال الكهربائية.")