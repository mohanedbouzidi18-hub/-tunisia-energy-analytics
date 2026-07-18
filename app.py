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

def calculate_risk(temp, hour):
    heat = (temp - 20) * 0.02
    peak = 0.3 if 14 <= hour <= 18 else 0
    return min(max(0.1 + heat + peak + random.uniform(-0.02, 0.02), 0.05), 0.95)



st.write("") # مسافة إضافية
st.markdown("<p class='big-font'>⚡ TUNISIA ENERGY ANALYTICS ⚡</p>", unsafe_allow_html=True)
region = st.selectbox("🌍 اختر الولاية:", tunisia_states)
# --- 3 صناديق منفصلة (حرارة، وقت، تاريخ) ---
current_time = datetime.now() + timedelta(hours=1)

# تأكد أن هذا الجزء كله داخل دالة واحدة
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown(f"""
        <div style="background-color: #1e90ff; padding: 15px; border-radius: 10px; text-align: center; color: white; font-weight: bold;">
            🌡️ الحرارة: {live_temp:.1f}°C
        </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown(f"""
        <div style="background-color: #1e90ff; padding: 15px; border-radius: 10px; text-align: center; color: white; font-weight: bold;">
            🕒 الوقت: {current_time.strftime('%H:%M')}
        </div>
    """, unsafe_allow_html=True)

with col_c:
    st.markdown(f"""
        <div style="background-color: #1e90ff; padding: 15px; border-radius: 10px; text-align: center; color: white; font-weight: bold;">
            📅 التاريخ: {current_time.strftime('%d/%m/%Y')}
        </div>
    """, unsafe_allow_html=True)

st.write("") # مسافة إضافية
live_temp = get_live_temp(region)
col1, col2 = st.columns(2)
temp = col1.slider("🌡️ الحرارة المعدلة:", 20.0, 50.0, float(max(20.0, min(50.0, live_temp))))
hour = col2.number_input("⏰ الساعة:", 0, 23, value=current_time.hour)
p_val = calculate_risk(temp, hour)
status_color = "#ff4b4b" if p_val > 0.7 else ("#ffa500" if p_val > 0.4 else "#58a6ff")
st.write(f"### نسبة الخطر المتوقعة: {p_val:.2%}")
st.progress(p_val)
if st.button("🚀 تشغيل التنبؤ"):
    st.session_state.history.append({"الوقت": current_time.strftime("%H:%M"), "الولاية": region, "الخطر": f"{p_val:.2%}"})
    st.success("تم الحفظ!")
col_a, col_b = st.columns(2)
with col_a:
    df = pd.DataFrame({'T': np.linspace(20, 50, 20), 'R': [calculate_risk(t, hour) for t in np.linspace(20, 50, 20)]})
    st.plotly_chart(px.area(df, x='T', y='R', template="plotly_dark", title="تطور الخطر حسب الحرارة"), use_container_width=True)
with col_b:
    st.plotly_chart(px.pie(values=[p_val, 1-p_val], names=['خطر', 'استقرار'], hole=0.7, 
                    color_discrete_sequence=[status_color, "#333"], title="مؤشر الحالة الحالي"), use_container_width=True)
st.subheader("📜 سجل التنبؤات")
st.dataframe(pd.DataFrame(st.session_state.history).tail(5), use_container_width=True)
st.subheader("⚠️ الأسباب التقنية المؤدية لقطع الكهرباء")

# تصميم بطاقات الأسباب بشكل احترافي ومقروء
st.markdown("""
<div style="display: flex; gap: 15px; flex-wrap: wrap; margin-top: 15px;">
    <div style="flex: 1; min-width: 250px; background-color: #1e1e2f; padding: 20px; border-radius: 12px; border-right: 5px solid #ff4b4b;">
        <h4 style="color: #ff4b4b; margin-top: 0;">🔥 الإجهاد الحراري للمحولات</h4>
        <p style="color: #cfcfdf; font-size: 15px; line-height: 1.6;">
            الارتفاع المفرط في درجات الحرارة يؤدي إلى تمدد الزيوت العازلة داخل المحولات، مما قد يسبب تلفاً للمكونات الداخلية للشبكة.
        </p>
    </div>
    <div style="flex: 1; min-width: 250px; background-color: #1e1e2f; padding: 20px; border-radius: 12px; border-right: 5px solid #ffa500;">
        <h4 style="color: #ffa500; margin-top: 0;">⚡ ذروة الاستهلاك اليومي</h4>
        <p style="color: #cfcfdf; font-size: 15px; line-height: 1.6;">
            يحدث ضغط هائل على المولدات خلال ساعات الذروة (خاصة من الساعة 14:00 إلى 18:00) بسبب التشغيل المكثف لأجهزة التكييف.
        </p>
    </div>
    <div style="flex: 1; min-width: 250px; background-color: #1e1e2f; padding: 20px; border-radius: 12px; border-right: 5px solid #58a6ff;">
        <h4 style="color: #58a6ff; margin-top: 0;">🛠️ أعمال الصيانة الطارئة</h4>
        <p style="color: #cfcfdf; font-size: 15px; line-height: 1.6;">
            تقوم الفرق الفنية بقطع التيار بشكل جزئي ومؤقت لحماية الشبكة من الانهيار الكامل وتخفيف الأحمال الزائدة عن المناطق الحرجّة.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)