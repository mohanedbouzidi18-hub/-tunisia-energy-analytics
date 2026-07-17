import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import random

# إعداد الصفحة
st.set_page_config(page_title="Tunisia Energy Pro", page_icon="⚡", layout="wide")

# تنسيق CSS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background: linear-gradient(135deg, #1a0a2e, #0b0e14); color: white; }
    [data-testid="stSidebar"] { background: #161b22; border-right: 1px solid #58a6ff; }
    [data-testid="stSidebar"] h2 { color: #58a6ff !important; }
    [data-testid="stSidebar"] label { color: #58a6ff !important; font-weight: bold; }
    h1 { color: #58a6ff !important; text-align: center; font-weight: 900; }
    h3 { color: #58a6ff !important; text-align: center; }
    div.stButton > button { background-color: #58a6ff !important; color: white !important; border-radius: 8px !important; width: 100%; border: none !important; }
    .stSlider [data-baseweb=slider] { color: #58a6ff !important; }
    div[role="slider"] { background-color: #58a6ff !important; }
    div[data-baseweb="select"] > div { border-color: #58a6ff !important; }
    div[data-baseweb="input"] > div { border-color: #58a6ff !important; }
    </style>
    """, unsafe_allow_html=True)

# دالة حساب الخطر الواقعية
def calculate_risk(temp, hour, region):
    region_weights = {'Tunis': 0.15, 'Sousse': 0.12, 'Mahdia': 0.08, 'Sidi Bou Zid': 0.05, 'Sfax': 0.10}
    heat_impact = (temp - 20) * 0.02
    peak_impact = 0.3 if 14 <= hour <= 18 else 0
    base_risk = region_weights.get(region, 0.05) + heat_impact + peak_impact
    noise = random.uniform(-0.02, 0.02)
    return min(max(base_risk + noise, 0.05), 0.95)

if 'history' not in st.session_state: st.session_state.history = []
# الواجهة الرئيسية
st.markdown("<h1>⚡ TUNISIA ENERGY ANALYTICS ⚡</h1>", unsafe_allow_html=True)

# التوقيت المباشر
from datetime import datetime, timedelta

# هذا السطر يضيف ساعة واحدة للتوقيت الحالي لتصحيح الفرق
# التوقيت المباشر مع تغيير اللون تلقائياً
# --- حساب الوقت والحالة الذكية ---
tunis_time = datetime.utcnow() + timedelta(hours=1)
current_hour = tunis_time.hour

# 1. تحديد اللون والنص والحالة بناءً على الساعة
if 14 <= current_hour < 16:
    status_color = "🔴"          # أحمر
    status_text = "أغلب مقصوص"
    progress_value = 0.9          
    border_color = "#ff4b4b"      
elif (16 <= current_hour < 20) or (11 <= current_hour < 14):
    status_color = "🟠"           # برتقالي
    status_text = "عادي"
    progress_value = 0.5          
    border_color = "#ffa500"      
else:
    status_color = "🟢"           # أخضر (للحالة المستقرة)
    status_text = "نسبة قليلة"
    progress_value = 0.1          
    border_color = "#58a6ff"      

# 2. عرض الساعة مع شريط التقدم والحالة
st.markdown(f"""
    <div style="text-align: center; padding: 15px; background: rgba(0,0,0,0.2); border-radius: 15px; border: 2px solid {border_color}; margin-bottom: 25px;">
        
        <div style="margin-bottom: 10px;">
            <h3 style="color: white; margin: 0;">🕒 {tunis_time.strftime("%H:%M")} | {tunis_time.strftime("%d %B %Y")}</h3>
        </div>

        <div style="width: 100%; height: 20px; background-color: #333; border-radius: 10px; overflow: hidden; margin-bottom: 10px;">
            <div style="width: {progress_value*100}%; height: 100%; background-color: {border_color}; transition: width 0.5s;"></div>
        </div>

        <div style="color: white; font-size: 1.1em;">
            الحالة: <strong style="color: {border_color};">{status_color} {status_text}</strong>
        </div>
        
    </div>
""", unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ Control Panel")
    region = st.selectbox("🌍 المنطقة:", ['Tunis', 'Sousse', 'Mahdia', 'Sidi Bou Zid', 'Sfax'])
    temp = st.slider("🌡️ الحرارة (°C):", 20, 50, 30)
    hour = st.number_input("⏰ الساعة:", 0, 23)
    if st.button("🚀 تشغيل التنبؤ"):
        prob = calculate_risk(temp, hour, region)
        st.session_state.history.append({"الوقت": datetime.now().strftime("%H:%M"), "المنطقة": region, "الخطر": f"{prob:.2%}"})
        # الرسوم البيانية
temps = np.linspace(20, 50, 30)
probs = [calculate_risk(t, hour, region) for t in temps]
df_area = pd.DataFrame({'Temperature': temps, 'Risk': probs})

st.subheader("📈 تحليل التأثير الزمني للحرارة")
fig_area = px.area(df_area, x='Temperature', y='Risk', template="plotly_dark")
fig_area.update_traces(line=dict(color='#58a6ff', width=3), fill='tozeroy', fillcolor='rgba(88, 166, 255, 0.15)')
fig_area.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=20, b=20), height=350)
st.plotly_chart(fig_area, use_container_width=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("📊 نسبة الخطر الحالية")
    current_prob = calculate_risk(temp, hour, region)
    df_pie = pd.DataFrame({'Status': ['Risk', 'Stable'], 'Value': [current_prob, 1-current_prob]})
    fig_pie = px.pie(df_pie, values='Value', names='Status', hole=0.7, color_discrete_map={'Risk': '#58a6ff', 'Stable': '#1a0a2e'})
    fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("📜 سجل التنبؤات الحديثة")
    st.dataframe(pd.DataFrame(st.session_state.history).tail(5), use_container_width=True)
    # قسم الأسباب
st.write("---")
st.subheader("💡 تحليل الأسباب التقنية لانقطاع التيار")
st.markdown("""
<div style="background-color: rgba(88, 166, 255, 0.05); padding: 25px; border-radius: 20px; border-left: 5px solid #58a6ff;">
    <ul style="list-style-type: none; padding-left: 0;">
        <li style="margin-bottom: 15px;">🔹 <b>الإجهاد الحراري:</b> زيادة الطلب على التكييف تضغط على المحولات.</li>
        <li style="margin-bottom: 15px;">🔹 <b>ذروة الاستهلاك:</b> الفترة بين 14:00 و 18:00 هي الأكثر خطورة.</li>
        <li style="margin-bottom: 15px;">🔹 <b>صيانة الشبكة:</b> تدخلات تقنية ضرورية لاستقرار التيار.</li>
        <li style="margin-bottom: 15px;">🔹 <b>عوامل جوية:</b> تأثيرات التقلبات المناخية على خطوط النقل.</li>
    </ul>
</div>
""", unsafe_allow_html=True)