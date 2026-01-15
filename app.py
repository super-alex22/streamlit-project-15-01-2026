import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Safe & Secure Gradebook", page_icon="🛡️", layout="wide")

# 2. Authentication System (Same as before)
def check_password():
    def password_entered():
        if st.session_state["password"] == "admin123":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔒 Access Restricted")
        st.text_input("Enter Teacher Password:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Enter Teacher Password:", type="password", on_change=password_entered, key="password")
        st.error("😕 Wrong password.")
        return False
    return True

if not check_password():
    st.stop()

# 3. Data Initialization
if "student_records" not in st.session_state:
    st.session_state.student_records = {
        "Ivan": [{'id': 1, 'value': 6, 'type': 'Test', 'date': '2026-01-10'}],
        "Maria": [{'id': 2, 'value': 6, 'type': 'Final Exam', 'date': '2026-01-12'}]
    }
if "id_counter" not in st.session_state:
    st.session_state.id_counter = 3

grade_types = {
    "Active Participation": 0.5, "Homework": 1.0, "Oral Test": 1.5,
    "Test": 2.0, "Project": 2.0, "Control Work": 2.5, "Final Exam": 3.0
}
grade_values = {
    "Excellent (6)": 6, "Very Good (5)": 5, "Good (4)": 4, 
    "Satisfactory (3)": 3, "Poor (2)": 2
}

# --- DIALOGS (Confirmations) ---

@st.dialog("Confirm Grade Addition")
def confirm_add_dialog(student, grade_label, category, date):
    st.write(f"Are you sure you want to add this grade to **{student}**?")
    st.write(f"**Grade:** {grade_label} | **Type:** {category} | **Date:** {date}")
    if st.button("Yes, add to records", use_container_width=True):
        val = grade_values[grade_label]
        st.session_state.student_records[student].append({
            'id': st.session_state.id_counter,
            'value': val,
            'type': category,
            'date': date.strftime("%Y-%m-%d")
        })
        st.session_state.id_counter += 1
        st.toast(f"Logged {val} for {student}!", icon="📝") #
        if val == 6: st.balloons()
        st.rerun()

@st.dialog("Confirm Deletion")
def confirm_delete_dialog(record_id):
    st.warning(f"Are you absolutely sure? This will permanently delete record ID: {record_id}.")
    if st.button("Yes, delete it forever", type="primary", use_container_width=True):
        for name in st.session_state.student_records:
            st.session_state.student_records[name] = [
                r for r in st.session_state.student_records[name] if r['id'] != record_id
            ]
        st.toast("Record successfully deleted!", icon="🗑️")
        st.rerun()

# --- MAIN INTERFACE ---
st.title("🛡️ The Unstoppable Gradebook")

# Input Section
st.subheader("📥 Log New Assignment")
col1, col2, col3, col4 = st.columns(4)

with col1:
    target_s = st.selectbox("Student:", list(st.session_state.student_records.keys()))
with col2:
    as_type = st.selectbox("Type:", list(grade_types.keys()))
with col3:
    g_label = st.selectbox("Grade:", list(grade_values.keys()))
with col4:
    target_date = st.date_input("Date:", value=datetime.now())

if st.button("Log Grade", use_container_width=True):
    # This triggers the confirmation pop-up
    confirm_add_dialog(target_s, g_label, as_type, target_date)

st.divider()

# --- AUDIT LOG & DELETION ---
st.header("📜 Global Audit Log")
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
    
    st.subheader("🗑️ Entry Removal")
    record_to_del = st.selectbox("Select ID to remove:", options=df["ID"].tolist())
    if st.button("Remove Selected Entry", type="primary"):
        # This triggers the confirmation pop-up
        confirm_delete_dialog(record_to_del)
else:
    st.info("No logs available yet.")
