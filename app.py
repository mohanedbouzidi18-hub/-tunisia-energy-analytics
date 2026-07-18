# PART 1: الاستيراد والإعدادات
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import random
import requests

st.set_page_config(page_title="Tunisia Energy Pro", layout="wide")
if 'history' not in st.session_state: st.session_state.history = []

# PART 2: تعريف الدوال
def get_live_temp(region):
    API_KEY = "abcdea1d329150e0d98cee0fd38c3576"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={region},TN&appid={API_KEY}&units=metric"
    try: return requests.get(url).json()['main']['temp']
    except: return 30.0

def calculate_risk(temp, hour):
    heat = (temp - 20) * 0.02
    peak = 0.3 if 14 <= hour <= 18 else 0
    return min(max(0.1 + heat + peak + random.uniform(-0.02, 0.02), 0.05), 0.95)

# PART 3: تهيئة البيانات والولاية
tunisia_states = ["Ariana", "Beja", "Ben Arous", "Bizerte", "Gabes", "Gafsa", "Jendouba", "Kairouan", "Kasserine", "Kebili", "Kef", "Mahdia", "Manouba", "Medenine", "Monastir", "Nabeul", "Sfax", "Sidi Bou Zid", "Siliana", "Sousse", "Tataouine", "Tozeur", "Tunis", "Zaghouan"]
region = st.selectbox("🌍 اختر الولاية:", tunisia_states)
live_temp = get_live_temp(region)
current_time = datetime.now() + timedelta(hours=1)

# PART 4: الصناديق الثلاثة في الأعلى (مع تغيير لون الحرارة)
if 45 <= live_temp <= 55: box_color = "#ff4b4b"
elif 35 <= live_temp <= 44: box_color = "#ffa500"
else: box_color = "#28a745"

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown(f"<div style='background-color: {box_color}; padding: 15px; border-radius: 10px; text-align: center; color: white; font-weight: bold;'>🌡️ الحرارة: {live_temp:.1f}°C</div>", unsafe_allow_html=True)
with col_b:
    st.markdown(f"<div style='background-color: #1e90ff; padding: 15px; border-radius: 10px; text-align: center; color: white; font-weight: bold;'>🕒 الوقت: {current_time.strftime('%H:%M')}</div>", unsafe_allow_html=True)
with col_c:
    st.markdown(f"<div style='background-color: #1e90ff; padding: 15px; border-radius: 10px; text-align: center; color: white; font-weight: bold;'>📅 التاريخ: {current_time.strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)

# PART 5: العنوان في الوسط
st.markdown("<br><p style='text-align: center; font-size:40px; font-weight: bold; color: #58a6ff;'>⚡ TUNISIA ENERGY ANALYTICS ⚡</p>", unsafe_allow_html=True)

# PART 6: مدخلات المستخدم
col1, col2 = st.columns(2)
temp = col1.slider("🌡️ الحرارة المعدلة:", 20.0, 50.0, float(max(20.0, min(50.0, live_temp))))
hour = col2.number_input("⏰ الساعة:", 0, 23, value=current_time.hour)

# PART 7: التنبؤ وعرض النتيجة
p_val = calculate_risk(temp, hour)
status_color = "#ff4b4b" if p_val > 0.7 else ("#ffa500" if p_val > 0.4 else "#58a6ff")
st.write(f"### نسبة الخطر المتوقعة: {p_val:.2%}")
st.progress(p_val)
if st.button("🚀 تشغيل التنبؤ"):
    st.session_state.history.append({"الوقت": current_time.strftime("%H:%M"), "الولاية": region, "الخطر": f"{p_val:.2%}"})
    st.success("تم الحفظ!")

# PART 8: الرسوم البيانية
c1, c2 = st.columns(2)
df = pd.DataFrame({'T': np.linspace(20, 50, 20), 'R': [calculate_risk(t, hour) for t in np.linspace(20, 50, 20)]})
c1.plotly_chart(px.area(df, x='T', y='R', template="plotly_dark", title="تطور الخطر"), use_container_width=True)
c2.plotly_chart(px.pie(values=[p_val, 1-p_val], names=['خطر', 'استقرار'], hole=0.7, color_discrete_sequence=[status_color, "#333"], title="المؤشر"), use_container_width=True)

# PART 9: سجل التنبؤات
st.subheader("📜 سجل التنبؤات")
st.dataframe(pd.DataFrame(st.session_state.history).tail(5), use_container_width=True)

# PART 10: الأسباب التقنية (تصميم بطاقات)
st.subheader("⚠️ الأسباب التقنية المؤدية لقطع الكهرباء")
st.markdown("""
<div style="display: flex; gap: 20px;">
    <div style="flex: 1; padding: 20px; background-color: #1a1a2e; border-radius: 10px; border-bottom: 5px solid #ff4b4b;"><h4>🔥 الإجهاد الحراري</h4><p>تلف المحولات بسبب الحرارة.</p></div>
    <div style="flex: 1; padding: 20px; background-color: #1a1a2e; border-radius: 10px; border-bottom: 5px solid #ffa500;"><h4>⚡ ذروة الاستهلاك</h4><p>ضغط عالي من 14:00 إلى 18:00.</p></div>
    <div style="flex: 1; padding: 20px; background-color: #1a1a2e; border-radius: 10px; border-bottom: 5px solid #58a6ff;"><h4>🛠️ الصيانة الطارئة</h4><p>تدخلات دورية لحماية الشبكة.</p></div>
</div>
""", unsafe_allow_html=True)