import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Advanced Weighted Gradebook", page_icon="⚖️")

# 2. Data Initialization
# Each student has a list of dictionaries: {'value': grade, 'type': category}
if "student_records" not in st.session_state:
    st.session_state.student_records = {
        "Ivan": [{'value': 6, 'type': 'Active Participation'}, {'value': 4, 'type': 'Test'}],
        "Maria": [{'value': 6, 'type': 'Final Exam'}, {'value': 5, 'type': 'Control Work'}],
        "Georgi": [{'value': 2, 'type': 'Control Work'}, {'value': 5, 'type': 'Homework'}],
        "Elena": [{'value': 6, 'type': 'Homework'}, {'value': 6, 'type': 'Project'}]
    }

# 3. Grading Categories and their "Weights" (Influence on final grade)
grade_types = {
    "Active Participation": 0.5,
    "Homework": 1.0,
    "Oral Test": 1.5,
    "Test": 2.0,
    "Project": 2.0,
    "Control Work": 2.5,
    "Final Exam": 3.0
}

grade_values = {
    "Excellent (6)": 6,
    "Very Good (5)": 5,
    "Good (4)": 4,
    "Satisfactory (3)": 3,
    "Poor (2)": 2
}

# --- SIDEBAR: Administrative Tools ---
st.sidebar.header("⚙️ Classroom Settings")
new_student = st.sidebar.text_input("Enroll New Student:")
if st.sidebar.button("Add to Roster"):
    if new_student and new_student not in st.session_state.student_records:
        st.session_state.student_records[new_student] = []
        st.sidebar.success(f"Student '{new_student}' added!")

st.sidebar.divider()
if st.sidebar.button("🔥 Factory Reset", help="Warning: This clears all grades!"):
    st.session_state.student_records = {k: [] for k in st.session_state.student_records}
    st.rerun()

# --- MAIN UI ---
st.title("👨‍🏫 Ultimate Weighted Gradebook")
st.write("Record assignments with different weights and track final semester performance.")

# --- DATA ENTRY SECTION ---
st.subheader("📥 Record New Grade")
col1, col2, col3 = st.columns(3)

with col1:
    target_student = st.selectbox("Student:", list(st.session_state.student_records.keys()))
with col2:
    assignment_type = st.selectbox("Category:", list(grade_types.keys()))
with col3:
    grade_label = st.selectbox("Grade:", list(grade_values.keys()))

if st.button("Save Entry", use_container_width=True):
    val = grade_values[grade_label]
    st.session_state.student_records[target_student].append({
        'value': val,
        'type': assignment_type
    })
    
    # Celebrate top achievements!
    if val == 6:
        st.balloons()
        st.success(f"Amazing! A 6 for {target_student} in {assignment_type}!")
    else:
        st.toast(f"Saved: {assignment_type} grade for {target_student}.")

st.divider()

# --- CALCULATIONS & RESULTS ---
st.header("📋 Semester Performance Report")

report_rows = []
for name, records in st.session_state.student_records.items():
    if records:
        # Math: Sum of (Grade * Weight) / Sum of Weights
        total_weighted_score = sum(r['value'] * grade_types[r['type']] for r in records)
        total_weights = sum(grade_types[r['type']] for r in records)
        weighted_avg = total_weighted_score / total_weights
        
        # Funny but professional status logic
        if weighted_avg >= 5.5: status = "🌟 Elite Scholar"
        elif weighted_avg >= 3.5: status = "✅ Good Standing"
        elif weighted_avg >= 3.0: status = "⚠️ At Risk"
        else: status = "🆘 Academic Probation"
    else:
        weighted_avg = 0.0
        status = "No Records Found"
    
    report_rows.append({
        "Student Name": name,
        "Total Tasks": len(records),
        "Weighted GPA": round(weighted_avg, 2),
        "Final Status": status
    })

# Main Table Display
final_df = pd.DataFrame(report_rows)
st.dataframe(final_df, use_container_width=True, hide_index=True)

# --- VISUALIZATION ---
st.subheader("📈 Class-wide Performance Comparison")
if not final_df.empty:
    chart_data = final_df.set_index("Student Name")["Weighted GPA"]
    st.bar_chart(chart_data)

# --- STUDENT DEEP DIVE (Optional but cool) ---
with st.expander("🔍 See Individual Progress Details"):
    selected_name = st.selectbox("Select student to inspect:", list(st.session_state.student_records.keys()))
    student_history = st.session_state.student_records[selected_name]
    if student_history:
        st.write(f"History for {selected_name}:")
        st.table(pd.DataFrame(student_history))
    else:
        st.write("No entries for this student yet.")

st.caption("Calculation Method: Weighted Arithmetic Mean. Final Exam weights 3x more than Homework.")
