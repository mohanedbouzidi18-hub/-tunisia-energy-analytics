import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import random
import requests
# --- إضافة في PART 1 ---
st.markdown("""<style>
    .big-font { font-size:32px !important; font-weight: bold; color: #58a6ff; }
    .status-box { padding: 20px; border-radius: 15px; text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 10px; }
    .stButton>button { font-size: 20px !important; height: 3em; width: 100%; }
</style>""", unsafe_allow_html=True)

current_hour = datetime.now().hour
theme = "#1a0a2e" if (current_hour < 6 or current_hour >= 20) else "#0b0e14"
st.set_page_config(page_title="Tunisia Energy Pro", page_icon="⚡", layout="wide")
st.markdown(f"<style>.stApp {{ background: {theme}; color: white; }}</style>", unsafe_allow_html=True)
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
# 4. الواجهة والولايات الـ 24
st.title("⚡ TUNISIA ENERGY ANALYTICS ⚡")

# قائمة الولايات الـ 24
tunisia_states = [
    "Ariana", "Beja", "Ben Arous", "Bizerte", "Gabes", "Gafsa", "Jendouba", 
    "Kairouan", "Kasserine", "Kebili", "Kef", "Mahdia", "Manouba", "Medenine", 
    "Monastir", "Nabeul", "Sfax", "Sidi Bou Zid", "Siliana", "Sousse", 
    "Tataouine", "Tozeur", "Tunis", "Zaghouan"
]

region = st.selectbox("🌍 اختر الولاية:", tunisia_states)
live_temp = get_live_temp(region)
# تحديد اللون بناءً على درجة الحرارة الحالية
if 45 <= live_temp <= 50:
    btn_color = "#ff4b4b"  # أحمر
    status_text = "حالة حرارية قصوى"
elif 35 <= live_temp <= 44:
    btn_color = "#ffa500"  # برتقالي
    status_text = "حالة حرارية معتدلة"
else:
    btn_color = "#58a6ff"  # أزرق
    status_text = "حالة حرارية طبيعية"

# عرض الزر التفاعلي
st.markdown(f"""
    <div style="background-color: {btn_color}; padding: 15px; border-radius: 10px; text-align: center; color: white; font-weight: bold;">
        🌡️ الحرارة: {live_temp:.1f}°C | 🕒 الوقت: {datetime.now().strftime('%H:%M')} | 📅 التاريخ: {datetime.now().strftime('%d/%m/%Y')}
        <br> {status_text}
    </div>
""", unsafe_allow_html=True)
st.write("") # مسافة إضافية
safe_temp = float(max(20.0, min(50.0, live_temp)))
col1, col2 = st.columns(2)
temp = col1.slider("🌡️ الحرارة (°C):", 20.0, 50.0, safe_temp)
hour = col2.number_input("⏰ الساعة:", 0, 23, value=datetime.now().hour)
p_val = calculate_risk(temp, hour, region)
status_color = "#ff4b4b" if p_val > 0.7 else ("#ffa500" if p_val > 0.4 else "#58a6ff")
st.markdown(f"### الحالة: <span style='color:{status_color}'>{'حرج' if p_val > 0.7 else 'عادي'}</span>", unsafe_allow_html=True)
st.progress(p_val)
if st.button("🚀 تشغيل التنبؤ"):
    st.session_state.history.append({
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
st.markdown("""
- **الإجهاد الحراري:** يؤدي لتمدد وتلف المحولات.
- **ذروة الاستهلاك:** ضغط عالٍ جداً (14:00 - 18:00).
- **صيانة الشبكة:** تدخلات فنية ضرورية لاستقرار النظام.
""")