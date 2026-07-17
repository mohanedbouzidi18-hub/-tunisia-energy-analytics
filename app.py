import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Tunisia Energy Pro", page_icon="⚡", layout="wide")

# تنسيق CSS
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1a0a2e, #0b0e14); color: white; }
    h1 { color: #58a6ff !important; text-align: center; font-weight: 900; }
    h3 { color: #58a6ff !important; }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []
def calculate_risk(temp, hour, region):
    region_weights = {'Tunis': 0.15, 'Sousse': 0.12, 'Mahdia': 0.08, 'Sidi Bou Zid': 0.05, 'Sfax': 0.10}
    heat_impact = (temp - 20) * 0.02
    peak_impact = 0.3 if 14 <= hour <= 18 else 0
    base_risk = region_weights.get(region, 0.05) + heat_impact + peak_impact
    return min(max(base_risk + random.uniform(-0.02, 0.02), 0.05), 0.95)

st.markdown("<h1>⚡ TUNISIA ENERGY ANALYTICS ⚡</h1>", unsafe_allow_html=True)
# أدوات التحكم في الواجهة الرئيسية
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
region = col_ctrl1.selectbox("🌍 المنطقة:", ['Tunis', 'Sousse', 'Mahdia', 'Sidi Bou Zid', 'Sfax'])
temp = col_ctrl2.slider("🌡️ الحرارة (°C):", 20, 50, 30)
hour = col_ctrl3.number_input("⏰ الساعة:", 0, 23)
tunis_time = datetime.utcnow() + timedelta(hours=1)
# إضافة التنبؤ للتاريخ تلقائياً عند تغيير أي قيمة
prob = calculate_risk(temp, hour, region)
if not st.session_state.history or st.session_state.history[-1]['الخطر'] != f"{prob:.2%}":
    st.session_state.history.append({"الوقت": tunis_time.strftime("%H:%M"), "المنطقة": region, "الخطر": f"{prob:.2%}"})

st.info(f"🕒 {tunis_time.strftime('%H:%M')} | المنطقة: {region} | نسبة الخطر المقدرة: {prob:.2%}")
st.subheader("📈 تحليل التأثير الزمني للحرارة")
temps = np.linspace(20, 50, 30)
probs = [calculate_risk(t, hour, region) for t in temps]
df_area = pd.DataFrame({'Temperature': temps, 'Risk': probs})

fig_area = px.area(df_area, x='Temperature', y='Risk', template="plotly_dark")
fig_area.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=350)
st.plotly_chart(fig_area, use_container_width=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("📊 نسبة الخطر الحالية")
    fig_pie = px.pie(values=[prob, 1-prob], names=['Risk', 'Stable'], hole=0.7, color_discrete_map={'Risk': '#58a6ff', 'Stable': '#1a0a2e'})
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("📜 سجل التنبؤات")
    st.dataframe(pd.DataFrame(st.session_state.history).tail(5), use_container_width=True)

st.write("---")
st.markdown("💡 **تحليل الأسباب:** الإجهاد الحراري، ذروة الاستهلاك، وصيانة الشبكة.")
