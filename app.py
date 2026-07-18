import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import random
import requests

st.set_page_config(page_title="Tunisia Energy Pro", layout="wide")
st.markdown("""<style>
    .big-font { font-size:32px !important; font-weight: bold; color: #58a6ff; }
    .status-box { padding: 20px; border-radius: 15px; text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 20px; }
</style>""", unsafe_allow_html=True)
if 'history' not in st.session_state: st.session_state.history = []
def get_live_temp(region):
    API_KEY = "abcdea1d329150e0d98cee0fd38c3576"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={region},TN&appid={API_KEY}&units=metric"
    try: return requests.get(url).json()['main']['temp']
    except: return 30.0
tunisia_states = ["Ariana", "Beja", "Ben Arous", "Bizerte", "Gabes", "Gafsa", "Jendouba", "Kairouan", "Kasserine", "Kebili", "Kef", "Mahdia", "Manouba", "Medenine", "Monastir", "Nabeul", "Sfax", "Sidi Bou Zid", "Siliana", "Sousse", "Tataouine", "Tozeur", "Tunis", "Zaghouan"]

def calculate_risk(temp, hour, region):
    heat = (temp - 20) * 0.02
    peak = 0.3 if 14 <= hour <= 18 else 0
    return min(max(0.1 + heat + peak + random.uniform(-0.02, 0.02), 0.05), 0.95)
st.markdown("<p class='big-font'>⚡ TUNISIA ENERGY ANALYTICS ⚡</p>", unsafe_allow_html=True)
region = st.selectbox("🌍 اختر الولاية:", tunisia_states)
live_temp = get_live_temp(region)
current_time = datetime.now() - timedelta(hours=1)
if 45 <= live_temp <= 50: box_style = "background-color: #ff0000; color: white;" 
elif 35 <= live_temp <= 44: box_style = "background-color: #ff8c00; color: white;"
else: box_style = "background-color: #1e90ff; color: white;"

st.markdown(f"""<div class='status-box' style='{box_style}'>
    🌡️ الحرارة: {live_temp:.1f}°C | 🕒 الوقت: {current_time.strftime('%H:%M')} | 📅 التاريخ: {current_time.strftime('%d/%m/%Y')}
</div>""", unsafe_allow_html=True)
col1, col2 = st.columns(2)
temp = col1.slider("🌡️ الحرارة المعدلة:", 20.0, 50.0, float(max(20.0, min(50.0, live_temp))))
hour = col2.number_input("⏰ الساعة:", 0, 23, value=current_time.hour)
p_val = calculate_risk(temp, hour, region)
st.write(f"### نسبة الخطر المتوقعة: {p_val:.2%}")
st.progress(p_val)
if st.button("🚀 تشغيل التنبؤ"):
    st.session_state.history.append({"الوقت": current_time.strftime("%H:%M"), "الولاية": region, "الخطر": f"{p_val:.2%}"})
    st.success("تم الحفظ!")
status_color = "#ff4b4b" if p_val > 0.7 else ("#ffa500" if p_val > 0.4 else "#58a6ff")
st.plotly_chart(px.pie(values=[p_val, 1-p_val], names=['Risk', 'Stable'], hole=0.7, 
                color_discrete_sequence=[status_color, "#333"]), use_container_width=True)
st.subheader("📜 سجل التنبؤات")
st.dataframe(pd.DataFrame(st.session_state.history).tail(5), use_container_width=True)
st.subheader("⚠️ أسباب انقطاع الكهرباء")
st.markdown("- **الإجهاد الحراري:** تلف المحولات.\n- **ذروة الاستهلاك:** الضغط (14:00-18:00).\n- **صيانة الشبكة:** تدخلات دورية.")