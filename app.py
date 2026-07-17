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
tunis_time = datetime.utcnow() + timedelta(hours=1)
if 14 <= tunis_time.hour < 16:
    s_color, s_text, p_val, b_color = "🔴", "أغلب مقصوص", 0.9, "#ff4b4b"
elif (16 <= tunis_time.hour < 20) or (11 <= tunis_time.hour < 14):
    s_color, s_text, p_val, b_color = "🟠", "عادي", 0.5, "#ffa500"
else:
    s_color, s_text, p_val, b_color = "🟢", "مستقر", 0.1, "#58a6ff"

st.markdown(f"""<div style="text-align: center; padding: 15px; border: 2px solid {b_color}; border-radius: 15px; margin-bottom: 25px;">
    <h3 style="color: white;">🕒 {tunis_time.strftime("%H:%M")} | {tunis_time.strftime("%d %B %Y")}</h3>
    <div style="width: 100%; height: 15px; background: #333; border-radius: 10px;"><div style="width: {p_val*100}%; height: 100%; background: {b_color}; border-radius: 10px;"></div></div>
    <div style="color: white;">الحالة: <strong style="color: {b_color};">{s_color} {s_text}</strong></div></div>""", unsafe_allow_html=True)
if st.button("🚀 تشغيل التنبؤ"):
    prob = calculate_risk(temp, hour, region)
    st.session_state.history.append({"الوقت": tunis_time.strftime("%H:%M"), "المنطقة": region, "الخطر": f"{prob:.2%}"})
    st.success(f"تم التنبؤ: نسبة الخطر {prob:.2%}")
col_a, col_b = st.columns([2, 1])
with col_a:
    st.subheader("📈 تحليل التأثير الزمني")
    temps = np.linspace(20, 50, 30)
    df_area = pd.DataFrame({'Temperature': temps, 'Risk': [calculate_risk(t, hour, region) for t in temps]})
    st.plotly_chart(px.area(df_area, x='Temperature', y='Risk', template="plotly_dark"), use_container_width=True)

with col_b:
    st.subheader("📊 نسبة الخطر")
    curr = calculate_risk(temp, hour, region)
    st.plotly_chart(px.pie(values=[curr, 1-curr], names=['Risk', 'Stable'], hole=0.7, color_discrete_map={'Risk': '#58a6ff'}), use_container_width=True)
    st.subheader("📜 سجل التنبؤات")
st.dataframe(pd.DataFrame(st.session_state.history).tail(5), use_container_width=True)
st.write("---")
st.subheader("💡 تحليل الأسباب التقنية")
st.markdown("""<div style="border-left: 5px solid #58a6ff; padding-left: 15px;">
    <ul><li><b>الإجهاد الحراري:</b> يقلل من كفاءة المحولات.</li>
    <li><b>ذروة الاستهلاك:</b> ضغط بين 14:00 و 18:00.</li>
    <li><b>صيانة الشبكة:</b> تدخلات ضرورية لاستقرار التيار.</li></ul></div>""", unsafe_allow_html=True)