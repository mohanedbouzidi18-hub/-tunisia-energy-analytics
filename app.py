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
# --- PART 4: الرسوم البيانية المرتبطة بالزر ---
# نضع زر التنبؤ في مكان واضح
if st.button("🚀 تشغيل التنبؤ"):
    # عند الضغط على الزر، نقوم بالحساب والعرض
    prob = calculate_risk(temp, hour, region)
    
    # تحديث السجل
    st.session_state.history.append({"الوقت": tunis_time.strftime("%H:%M"), "المنطقة": region, "الخطر": f"{prob:.2%}"})
    
    # عرض الرسوم البيانية فقط بعد الضغط على الزر
    st.subheader("📈 تحليل التأثير الزمني للحرارة")
    temps = np.linspace(20, 50, 30)
    probs = [calculate_risk(t, hour, region) for t in temps]
    df_area = pd.DataFrame({'Temperature': temps, 'Risk': probs})
    
    fig_area = px.area(df_area, x='Temperature', y='Risk', template="plotly_dark")
    fig_area.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=350)
    st.plotly_chart(fig_area, use_container_width=True)
    
    # عرض الـ Pie Chart أيضاً
    st.subheader("📊 نسبة الخطر الحالية")
    fig_pie = px.pie(values=[prob, 1-prob], names=['Risk', 'Stable'], hole=0.7, 
                     color_discrete_map={'Risk': '#58a6ff', 'Stable': '#1a0a2e'})
    fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', height=300)
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.info("👈 اضغط على 'تشغيل التنبؤ' لرؤية النتائج والرسوم البيانية")
# --- PART 3: التوقيت والحالة الذكية بالألوان ---
tunis_time = datetime.utcnow() + timedelta(hours=1)
current_hour = tunis_time.hour

# تحديد اللون والحالة
if 14 <= current_hour < 16:
    status_color, status_text, progress_value, border_color = "🔴", "أغلب مقصوص", 0.9, "#ff4b4b"
elif (16 <= current_hour < 20) or (11 <= current_hour < 14):
    status_color, status_text, progress_value, border_color = "🟠", "عادي", 0.5, "#ffa500"
else:
    status_color, status_text, progress_value, border_color = "🟢", "مستقر", 0.1, "#58a6ff"

# عرض الساعة وشريط الحالة
st.markdown(f"""
    <div style="text-align: center; padding: 15px; background: rgba(0,0,0,0.2); border-radius: 15px; border: 2px solid {border_color}; margin-bottom: 25px;">
        <h3 style="color: white; margin: 0;">🕒 {tunis_time.strftime("%H:%M")} | {tunis_time.strftime("%d %B %Y")}</h3>
        <div style="width: 100%; height: 15px; background-color: #333; border-radius: 10px; margin: 10px 0;">
            <div style="width: {progress_value*100}%; height: 100%; background-color: {border_color}; border-radius: 10px;"></div>
        </div>
        <div style="color: white;">الحالة: <strong style="color: {border_color};">{status_color} {status_text}</strong></div>
    </div>
""", unsafe_allow_html=True)
st.subheader("📈 تحليل التأثير الزمني للحرارة")
temps = np.linspace(20, 50, 30)
probs = [calculate_risk(t, hour, region) for t in temps]
df_area = pd.DataFrame({'Temperature': temps, 'Risk': probs})

fig_area = px.area(df_area, x='Temperature', y='Risk', template="plotly_dark")
fig_area.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=350)
st.plotly_chart(fig_area, use_container_width=True)

# --- PART 5: التحليلات والأسباب التقنية ---
# --- PART 5: نسبة الخطر والسجل ---
col_pie, col_hist = st.columns([1, 1])

with col_pie:
    st.subheader("📊 نسبة الخطر الحالية")
    # حساب الخطر الحالي بناءً على القيم المختارة
    curr_prob = calculate_risk(temp, hour, region)
    
    # الرسم الدائري (الذي اختفى)
    df_pie = pd.DataFrame({'Status': ['Risk', 'Stable'], 'Value': [curr_prob, 1-curr_prob]})
    fig_pie = px.pie(df_pie, values='Value', names='Status', hole=0.7, 
                     color_discrete_map={'Risk': '#58a6ff', 'Stable': '#1a0a2e'})
    fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', 
                          plot_bgcolor='rgba(0,0,0,0)', height=300)
    st.plotly_chart(fig_pie, use_container_width=True)

with col_hist:
    st.subheader("📜 سجل التنبؤات")
    st.dataframe(pd.DataFrame(st.session_state.history).tail(5), use_container_width=True)

# إضافة الأسباب التقنية كما طلبت
st.write("---")
st.subheader("💡 تحليل الأسباب التقنية لانقطاع التيار")
st.markdown("""
<div style="background-color: rgba(88, 166, 255, 0.05); padding: 20px; border-radius: 20px; border-left: 5px solid #58a6ff;">
    <ul style="list-style-type: none; padding-left: 0;">
        <li style="margin-bottom: 12px;">🔹 <b>الإجهاد الحراري:</b> الارتفاع الكبير في درجات الحرارة يرفع حرارة الكابلات.</li>
        <li style="margin-bottom: 12px;">🔹 <b>ذروة الاستهلاك (Peak Load):</b> زيادة الطلب المتزامن بين 14:00 و 18:00.</li>
        <li style="margin-bottom: 12px;">🔹 <b>نقص سعة الشبكة:</b> عجز الشبكة عن استيعاب الأحمال العالية.</li>
        <li style="margin-bottom: 12px;">🔹 <b>التقلبات الجهدية:</b> عدم استقرار التردد بسبب تغير الطلب.</li>
        <li style="margin-bottom: 12px;">🔹 <b>أعمال الصيانة الوقائية:</b> تدخلات ضرورية لسلامة المحولات.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
# --- الجزء الخاص بـ الزر والسجل ---
if st.button("🚀 تشغيل التنبؤ"):
    # 1. الحساب
    prob = calculate_risk(temp, hour, region)
    
    # 2. الحفظ في السجل (Session State)
    # نقوم بإضافة النتيجة الجديدة إلى القائمة
    new_entry = {"الوقت": tunis_time.strftime("%H:%M"), "المنطقة": region, "الخطر": f"{prob:.2%}"}
    st.session_state.history.append(new_entry)
    
    # 3. عرض النتيجة فوراً
    st.success(f"تم تسجيل التنبؤ بنجاح! الخطر الحالي: {prob:.2%}")

# --- عرض الجدول في الأسفل (سيعرض السجل المحدث) ---
st.subheader("📜 سجل التنبؤات الحديثة")
if st.session_state.history:
    # عرض آخر 5 تنبؤات
    history_df = pd.DataFrame(st.session_state.history).tail(5)
    st.dataframe(history_df, use_container_width=True)
else:
    st.write("لا يوجد تنبؤات سابقة.")