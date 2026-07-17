import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import random

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
# --- PART 4: زر التنبؤ والتحديث ---
# يجب تعريف الوقت هنا داخل الزر أو قبل استخدامه لضمان توفره
if st.button("🚀 تشغيل التنبؤ"):
    # حساب الوقت اللحظي عند الضغط
    current_time_now = datetime.utcnow() + timedelta(hours=1)
    
    # حساب الخطر
    prob = calculate_risk(temp, hour, region)
    
    # حفظ النتيجة في السجل
    st.session_state.history.append({
        "الوقت": current_time_now.strftime("%H:%M"), 
        "المنطقة": region, 
        "الخطر": f"{prob:.2%}"
    })
    
    st.success(f"تم التنبؤ بنجاح! نسبة الخطر: {prob:.2%}")
with col_a:
    st.subheader("📈 تحليل التأثير الزمني")
    temps = np.linspace(20, 50, 30)
    df_area = pd.DataFrame({'Temperature': temps, 'Risk': [calculate_risk(t, hour, region) for t in temps]})
    st.plotly_chart(px.area(df_area, x='Temperature', y='Risk', template="plotly_dark"), use_container_width=True)

with col_b:
    st.subheader("📊 نسبة الخطر الحالية")
    curr = calculate_risk(temp, hour, region)
    st.plotly_chart(px.pie(values=[curr, 1-curr], names=['Risk', 'Stable'], hole=0.7, color_discrete_map={'Risk': '#58a6ff', 'Stable': '#1a0a2e'}), use_container_width=True)
st.subheader("📜 سجل التنبؤات الحديثة")
st.dataframe(pd.DataFrame(st.session_state.history).tail(5), use_container_width=True)
st.write("---")
st.subheader("💡 تحليل الأسباب التقنية")
st.markdown("""<div style="border-left: 5px solid #58a6ff; padding-left: 15px;">
    <ul><li><b>الإجهاد الحراري:</b> يقلل من كفاءة المحولات.</li>
    <li><b>ذروة الاستهلاك:</b> ضغط عالٍ بين 14:00 و 18:00.</li>
    <li><b>نقص سعة الشبكة:</b> عجز عن استيعاب الأحمال العالية.</li>
    <li><b>التقلبات الجهدية:</b> عدم استقرار التردد بسبب الطلب.</li>
    <li><b>صيانة الشبكة:</b> تدخلات ضرورية لسلامة المحولات.</li></ul></div>""", unsafe_allow_html=True)