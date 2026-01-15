import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Pro Gradebook & GPA", page_icon="🎓")

# 2. Data Initialization
# We now store grades in a list for each student to calculate the average
if "student_records" not in st.session_state:
    st.session_state.student_records = {
        "Ivan": [6, 5, 4],
        "Maria": [6, 6, 5],
        "Georgi": [3, 4, 3],
        "Elena": [6, 5, 6]
    }

# Mapping grades to numerical values for math operations
grade_values = {
    "Excellent (6)": 6,
    "Very Good (5)": 5,
    "Good (4)": 4,
    "Satisfactory (3)": 3,
    "Poor (2)": 2
}

# --- SIDEBAR ---
st.sidebar.header("⚙️ Classroom Setup")
new_student = st.sidebar.text_input("New Student Name:")
if st.sidebar.button("Add to Class"):
    if new_student and new_student not in st.session_state.student_records:
        st.session_state.student_records[new_student] = []
        st.sidebar.success(f"{new_student} added to roster!")

if st.sidebar.button("🔥 Factory Reset"):
    st.session_state.student_records = {k: [] for k in st.session_state.student_records}
    st.rerun()

# --- MAIN UI ---
st.title("📊 Final Grade Calculator")
st.write("Record new grades and automatically calculate the final GPA for each student.")

# Input Section
st.subheader("📥 Quick Grade Entry")
col_s, col_g, col_b = st.columns([2, 2, 1])

with col_s:
    student = st.selectbox("Student:", list(st.session_state.student_records.keys()))
with col_g:
    grade_label = st.selectbox("Grade:", list(grade_values.keys()))
with col_b:
    st.write(" ") # Padding
    if st.button("Add Grade"):
        val = grade_values[grade_label]
        st.session_state.student_records[student].append(val)
        if val == 6: st.balloons()
        st.toast(f"Recorded {val} for {student}")

st.divider()

# --- FINAL GRADE CALCULATION ---
st.header("📋 Official Gradebook")

# Prepare data for the final table
report_data = []
for name, grades in st.session_state.student_records.items():
    if grades:
        avg = sum(grades) / len(grades)
        status = "✅ PASS" if avg >= 3.0 else "❌ FAIL"
    else:
        avg = 0.0
        status = "No Data"
    
    report_data.append({
        "Student Name": name,
        "Grades Count": len(grades),
        "Average Score": round(avg, 2),
        "Final Status": status
    })

# Display as a professional table
final_df = pd.DataFrame(report_data)
st.table(final_df)



# --- VISUALIZATION ---
st.subheader("📈 Performance Chart")
if not final_df.empty:
    chart_df = final_df.set_index("Student Name")["Average Score"]
    st.bar_chart(chart_df)

st.caption("Final grades are calculated using a simple arithmetic mean.")
