
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Lab Reports", layout="centered")

# --- Initialize session ---
if 'patients' not in st.session_state:
    st.session_state.patients = {}

st.title("برنامج التحاليل الطبية")
st.markdown("### تسجيل بيانات المريض")

# --- إدخال بيانات المريض ---
name = st.text_input("اسم المريض")
patient_id = st.text_input("الرقم التأميني")
report_date = st.date_input("التاريخ", value=date.today())

if st.button("تخزين المريض"):
    if name and patient_id:
        st.session_state.patients[patient_id] = {
            "name": name,
            "date": report_date,
            "tests": {}
        }
        st.success("تم تسجيل المريض")
    else:
        st.error("يرجى إدخال الاسم والرقم التأميني")

# --- عرض المرضى ---
st.markdown("### المرضى السابقين")
if st.session_state.patients:
    selected = st.selectbox("اختر مريضًا", options=st.session_state.patients.keys())
    selected_data = st.session_state.patients[selected]
    st.write(f"**اسم المريض:** {selected_data['name']}")
    st.write(f"**تاريخ التقرير:** {selected_data['date']}")

    # --- إدخال نتائج التحاليل ---
    st.markdown("### اختيار التحاليل وكتابة القيم")
    tests_list = ['Hemoglobin', 'WBC', 'Platelets', 'Glucose', 'Urea', 'Creatinine', 'ALT', 'AST']
    selected_tests = st.multiselect("اختر التحاليل المطلوبة", options=tests_list)

    results = {}
    for test in selected_tests:
        value = st.text_input(f"{test}:", key=test)
        if value:
            results[test] = value

    if st.button("حفظ النتائج"):
        st.session_state.patients[selected]["tests"] = results
        st.success("تم حفظ نتائج التحاليل")

    # --- عرض النتائج ---
    if st.session_state.patients[selected]["tests"]:
        st.markdown("### النتائج الحالية")
        df = pd.DataFrame.from_dict(st.session_state.patients[selected]["tests"], orient="index", columns=["القيمة"])
        st.table(df)

else:
    st.info("لم يتم تسجيل مرضى بعد.")
