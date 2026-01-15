import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="The Eternal Gradebook", page_icon="🕵️‍♂️", layout="wide")

# 2. Data Initialization with Timestamps
if "student_records" not in st.session_state:
    # Records now include 'date' for every entry
    st.session_state.student_records = {
        "Ivan": [{'value': 6, 'type': 'Active Participation', 'date': '2026-01-10 09:00'}],
        "Maria": [{'value': 6, 'type': 'Final Exam', 'date': '2026-01-12 14:30'}],
        "Georgi": [{'value': 2, 'type': 'Control Work', 'date': '2026-01-14 11:15'}],
        "Elena": [{'value': 5, 'type': 'Homework', 'date': '2026-01-15 08:45'}]
    }

# 3. Weights and Values Configuration
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

# --- SIDEBAR: Admin Tools ---
st.sidebar.header("🛠️ Admin Controls")
new_student = st.sidebar.text_input("Enroll Student Name:")
if st.sidebar.button("Register Student"):
    if new_student and new_student not in st.session_state.student_records:
        st.session_state.student_records[new_student] = []
        st.sidebar.success(f"Student '{new_student}' is now in the system.")

if st.sidebar.button("🔥 Absolute Reset"):
    st.session_state.student_records = {k: [] for k in st.session_state.student_records}
    st.rerun()

# --- MAIN UI ---
st.title("🕵️‍♂️ The Master Gradebook & Audit Log")
st.write("Track every grade, every category, and every second of academic progress.")

# Input Section
st.subheader("📥 Entry Point")
c1, c2, c3 = st.columns(3)

with c1:
    target_student = st.selectbox("Select Student:", list(st.session_state.student_records.keys()))
with c2:
    assignment_type = st.selectbox("Select Type:", list(grade_types.keys()))
with c3:
    grade_label = st.selectbox("Select Grade:", list(grade_values.keys()))

if st.button("Log Grade into History", use_container_width=True):
    val = grade_values[grade_label]
    # Adding the current time to the entry
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.student_records[target_student].append({
        'value': val,
        'type': assignment_type,
        'date': current_time
    })
    st.success(f"Entry confirmed for {target_student} at {current_time}!")
    if val == 6: st.balloons()

st.divider()

# --- THE ALL-SEEING LOG (Full History) ---
st.header("📜 Global Audit Log")
st.write("Here is the full list of all grades entered into the system, sorted by time.")

# Flattening the dictionary for a global view
all_entries = []
for student_name, entries in st.session_state.student_records.items():
    for record in entries:
        all_entries.append({
            "Timestamp": record['date'],
            "Student": student_name,
            "Type": record['type'],
            "Grade": record['value']
        })

if all_entries:
    full_history_df = pd.DataFrame(all_entries)
    # Sorting by timestamp so the latest is on top
    full_history_df = full_history_df.sort_values(by="Timestamp", ascending=False)
    st.dataframe(full_history_df, use_container_width=True, hide_index=True)
else:
    st.info("The history is currently empty. Start grading!")

st.divider()

# --- SEMESTER SUMMARY ---
st.header("📊 Semester Statistics")

report_rows = []
for name, records in st.session_state.student_records.items():
    if records:
        total_score = sum(r['value'] * grade_types[r['type']] for r in records)
        total_weight = sum(grade_types[r['type']] for r in records)
        weighted_avg = total_score / total_weight
    else:
        weighted_avg = 0.0
    
    report_rows.append({
        "Student": name,
        "Entries": len(records),
        "Weighted GPA": round(weighted_avg, 2)
    })

summary_df = pd.DataFrame(report_rows)
st.table(summary_df)

st.caption("Weighted GPA Formula: $Final = \\frac{\\sum (Grade_i \\times Weight_i)}{\\sum Weight_i}$")
