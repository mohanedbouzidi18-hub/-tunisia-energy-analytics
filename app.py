import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import random
import requests

# تحديد اللون حسب وقت اليوم
current_hour = datetime.now().hour
theme_color = "#1a0a2e" if (current_hour < 6 or current_hour >= 20) else "#0b0e14"

st.set_page_config(page_title="Tunisia Energy Pro", page_icon="⚡", layout="wide")
st.markdown(f"""<style>.stApp {{ background: {theme_color}; color: white; }}</style>""", unsafe_allow_html=True)
if 'history' not in st.session_state: st.session_state.history = []
API_KEY = "abcdea1d329150e0d98cee0fd38c3576"
def get_live_temp(region):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={region},TN&appid={API_KEY}&units=metric"
    try:
        return requests.get(url).json()['main']['temp']
    except:
        return 30.0
def calculate_risk(temp, hour, region):
    weights = {'Tunis': 0.15, 'Sousse': 0.12, 'Mahdia': 0.08, 'Sidi Bou Zid': 0.05, 'Sfax': 0.10}
    heat = (temp - 20) * 0.02
    peak = 0.3 if 14 <= hour <= 18 else 0
    return min(max(weights.get(region, 0.05) + heat + peak + random.uniform(-0.02, 0.02), 0.05), 0.95)
st.title("⚡ TUNISIA ENERGY ANALYTICS ⚡")
region = st.selectbox("🌍 المنطقة:", ['Tunis', 'Sousse', 'Mahdia', 'Sidi Bou Zid', 'Sfax'])
live_temp = get_live_temp(region)
col1, col2 = st.columns(2)
temp = col1.slider("🌡️ الحرارة (°C):", 20, 50, float(live_temp))
hour = col2.number_input("⏰ الساعة:", 0, 23, value=datetime.now().hour)
p_val = calculate_risk(temp, hour, region)
# اللون يتغير حسب نسبة الخطر (أحمر، برتقالي، أزرق)
status_color = "#ff4b4b" if p_val > 0.7 else ("#ffa500" if p_val > 0.4 else "#58a6ff")
st.markdown(f"### الحالة: <span style='color:{status_color}'>{'خطر مرتفع' if p_val > 0.7 else 'عادي'}</span>", unsafe_allow_html=True)
st.progress(p_val)
if st.button("🚀 تشغيل التنبؤ"):
    st.session_state.history.append({
        "التاريخ": datetime.now().strftime("%d/%m"),
        "الوقت": datetime.now().strftime("%H:%M"),
        "المنطقة": region,
        "الخطر": f"{p_val:.2%}"
    })
    st.success("تم تسجيل التنبؤ!")
col_a, col_b = st.columns([2, 1])
with col_a:
    df = pd.DataFrame({'T': np.linspace(20, 50, 20), 'R': [calculate_risk(t, hour, region) for t in np.linspace(20, 50, 20)]})
    st.plotly_chart(px.area(df, x='T', y='R', template="plotly_dark"), use_container_width=True)
with col_b:
    st.plotly_chart(px.pie(values=[p_val, 1-p_val], names=['Risk', 'Stable'], hole=0.7, color_discrete_sequence=[status_color, "#333"]), use_container_width=True)
    st.subheader("📜 سجل التنبؤات")
st.dataframe(pd.DataFrame(st.session_state.history).tail(5), use_container_width=True)
st.subheader("⚠️ أسباب انقطاع الكهرباء")
st.markdown("- **الإجهاد الحراري:** يسبب تمدد وتلف المحولات.\n- **ذروة الاستهلاك:** الضغط (14:00 - 18:00).\n- **صيانة الشبكة:** تدخلات فنية دورية.")