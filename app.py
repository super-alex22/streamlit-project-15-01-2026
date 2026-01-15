import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Gradebook Pro Max", page_icon="📈", layout="wide")

# 2. Data Initialization
if "student_records" not in st.session_state:
    st.session_state.student_records = {
        "Ivan": [{'id': 1, 'value': 6, 'type': 'Test', 'date': '2026-01-10 09:00'}],
        "Maria": [{'id': 2, 'value': 6, 'type': 'Final Exam', 'date': '2026-01-12 14:30'}]
    }
if "id_counter" not in st.session_state:
    st.session_state.id_counter = 3

# 3. Weights and Values
grade_types = {
    "Active Participation": 0.5, "Homework": 1.0, "Oral Test": 1.5,
    "Test": 2.0, "Project": 2.0, "Control Work": 2.5, "Final Exam": 3.0
}
grade_values = {
    "Excellent (6)": 6, "Very Good (5)": 5, "Good (4)": 4, 
    "Satisfactory (3)": 3, "Poor (2)": 2
}

# --- SIDEBAR: Admin ---
st.sidebar.header("⚙️ Settings")
new_student = st.sidebar.text_input("Enroll Student:")
if st.sidebar.button("Add to System"):
    if new_student and new_student not in st.session_state.student_records:
        st.session_state.student_records[new_student] = []
        st.sidebar.success(f"{new_student} is ready!")

# --- MAIN UI ---
st.title("🍎 Smart Class Auditor")

# --- SECTION 1: ADDING GRADES ---
st.subheader("📥 Add Performance Record")
col1, col2, col3 = st.columns(3)

with col1:
    target_s = st.selectbox("Student:", list(st.session_state.student_records.keys()))
with col2:
    as_type = st.selectbox("Type:", list(grade_types.keys()))
with col3:
    g_label = st.selectbox("Grade:", list(grade_values.keys()))

if st.button("Add Grade to Ledger", use_container_width=True):
    val = grade_values[g_label]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create record with unique ID for deletion tracking
    st.session_state.student_records[target_s].append({
        'id': st.session_state.id_counter,
        'value': val,
        'type': as_type,
        'date': now
    })
    st.session_state.id_counter += 1
    
    # POP-UP NOTIFICATIONS
    st.toast(f"Success! {target_s} received a {val}", icon="✅")
    if val == 6: st.balloons()

st.divider()

# --- SECTION 2: VIEWING & DELETING ---
st.header("📜 Audit Log & Correction")

# Flattening data for the table
all_entries = []
for name, records in st.session_state.student_records.items():
    for r in records:
        all_entries.append({
            "ID": r['id'], "Date": r['date'], "Student": name, 
            "Category": r['type'], "Score": r['value']
        })

if all_entries:
    df = pd.DataFrame(all_entries).sort_values(by="Date", ascending=False)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # DELETION LOGIC
    st.subheader("🗑️ Delete Incorrect Entry")
    # Creating a label for the selectbox to identify records
    record_to_del = st.selectbox(
        "Select record ID to remove:", 
        options=df["ID"].tolist(),
        format_func=lambda x: f"ID: {x} | {df[df['ID']==x]['Student'].values[0]} - {df[df['ID']==x]['Category'].values[0]}"
    )
    
    if st.button("Delete Record", type="primary"):
        for name in st.session_state.student_records:
            st.session_state.student_records[name] = [
                r for r in st.session_state.student_records[name] if r['id'] != record_to_del
            ]
        st.toast("Record deleted successfully!", icon="🗑️")
        st.rerun()
else:
    st.info("No records to display.")

st.divider()

# --- SECTION 3: ANALYTICS ---
st.header("📊 Final Weighted GPA")
stats = []
for name, records in st.session_state.student_records.items():
    if records:
        total = sum(r['value'] * grade_types[r['type']] for r in records)
        w_sum = sum(grade_types[r['type']] for r in records)
        avg = round(total / w_sum, 2)
    else: avg = 0.0
    stats.append({"Student": name, "GPA": avg})

st.table(pd.DataFrame(stats))
