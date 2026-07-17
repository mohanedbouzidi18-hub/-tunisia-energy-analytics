import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import random
import requests # لازم تزيد هذي

API_KEY = "abcdea1d329150e0d98cee0fd38c3576"
# PART 1: المكتبات

# PART 2: دالة جلب الطقس الحقيقي
def get_live_temp(region):
    # رابط API المجاني
    url = f"http://api.openweathermap.org/data/2.5/weather?q={region},TN&appid=abcdea1d329150e0d98cee0fd38c3576&units=metric"
    try:
        response = requests.get(url).json()
        return response['main']['temp']
    except:
        return 30.0 # إذا حدث خطأ، سيعود لـ 30 درجة تلقائياً# لازم تسجل في موقعهم وتجيب API Key

st.set_page_config(page_title="Tunisia Energy Pro", page_icon="⚡", layout="wide")
st.markdown("""<style>.stApp { background: linear-gradient(135deg, #1a0a2e, #0b0e14); color: white; }
    h1 { color: #58a6ff !important; text-align: center; font-weight: 900; }
    h3 { color: #58a6ff !important; }</style>""", unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []
def calculate_risk(temp, hour, region):
    region_weights = {'Tunis': 0.15, 'Sousse': 0.12, 'Mahdia': 0.08, 'Sidi Bou Zid': 0.05, 'Sfax': 0.10}
    heat_impact = (temp - 20) * 0.02
    peak_impact = 0.3 if 14 <= hour <= 18 else 0
    return min(max(region_weights.get(region, 0.05) + heat_impact + peak_impact + random.uniform(-0.02, 0.02), 0.05), 0.95)
st.markdown("<h1>⚡ TUNISIA ENERGY ANALYTICS ⚡</h1>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
region = c1.selectbox("🌍 المنطقة:", ['Tunis', 'Sousse', 'Mahdia', 'Sidi Bou Zid', 'Sfax'])
temp = c2.slider("🌡️ الحرارة (°C):", 20, 50, 30)
hour = c3.number_input("⏰ الساعة:", 0, 23)
current_time = datetime.utcnow() + timedelta(hours=1)
if 14 <= current_time.hour < 16:
    s_color, s_text, p_val, b_color = "🔴", "أغلب مقصوص", 0.9, "#ff4b4b"
elif (16 <= current_time.hour < 20) or (11 <= current_time.hour < 14):
    s_color, s_text, p_val, b_color = "🟠", "عادي", 0.5, "#ffa500"
else:
    s_color, s_text, p_val, b_color = "🟢", "مستقر", 0.1, "#58a6ff"

st.markdown(f"""<div style="text-align: center; padding: 15px; border: 2px solid {b_color}; border-radius: 15px; margin-bottom: 25px;">
    <h3 style="color: white;">🕒 {current_time.strftime("%H:%M")} | {current_time.strftime("%d %B %Y")}</h3>
    <div style="width: 100%; height: 15px; background: #333; border-radius: 10px;"><div style="width: {p_val*100}%; height: 100%; background: {b_color}; border-radius: 10px;"></div></div>
    <div style="color: white;">الحالة: <strong style="color: {b_color};">{s_color} {s_text}</strong></div></div>""", unsafe_allow_html=True)
if st.button("🚀 تشغيل التنبؤ"):
    prob = calculate_risk(temp, hour, region)
    time_now = datetime.utcnow() + timedelta(hours=1)
    st.session_state.history.append({"الوقت": time_now.strftime("%H:%M"), "المنطقة": region, "الخطر": f"{prob:.2%}"})
    st.success(f"تم التنبؤ بنجاح! نسبة الخطر: {prob:.2%}")
col_a, col_b = st.columns([2, 1])
with col_a:
    st.subheader("📈 تحليل التأثير الزمني")
    temps_range = np.linspace(20, 50, 30)
    df_area = pd.DataFrame({'Temperature': temps_range, 'Risk': [calculate_risk(t, hour, region) for t in temps_range]})
    st.plotly_chart(px.area(df_area, x='Temperature', y='Risk', template="plotly_dark"), use_container_width=True)

with col_b:
    st.subheader("📊 نسبة الخطر الحالية")
    curr_prob = calculate_risk(temp, hour, region)
    st.plotly_chart(px.pie(values=[curr_prob, 1-curr_prob], names=['Risk', 'Stable'], hole=0.7, color_discrete_map={'Risk': '#58a6ff', 'Stable': '#1a0a2e'}), use_container_width=True)
    st.subheader("📜 سجل التنبؤات الحديثة")
st.dataframe(pd.DataFrame(st.session_state.history).tail(5), use_container_width=True)
st.write("---")
st.subheader("💡 تحليل الأسباب التقنية")
st.markdown("""<div style="border-left: 5px solid #58a6ff; padding-left: 15px;">
    <ul><li><b>الإجهاد الحراري:</b> يقلل من كفاءة المحولات.</li>
    <li><b>ذروة الاستهلاك:</b> ضغط عالٍ بين 14:00 و 18:00.</li>
    <li><b>نقص سعة الشبكة:</b> عجز عن استيعاب الأحمال العالية.</li>
    <li><b>التقلبات الجهدية:</b> عدم استقرار التردد.</li>
    <li><b>صيانة الشبكة:</b> تدخلات ضرورية لسلامة المحولات.</li></ul></div>""", unsafe_allow_html=True)