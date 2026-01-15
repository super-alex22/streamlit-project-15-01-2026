import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Secure Gradebook & Audit", page_icon="🔐", layout="wide")

# 2. Basic Security System
def check_password():
    """Returns True if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == "admin123": # Change your password here!
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.title("🔒 Access Restricted")
        st.text_input("Enter Teacher Password:", type="password", on_change=password_entered, key="password")
        st.info("Hint: The default password is 'admin123'. Keep it secret, keep it safe!")
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error
        st.text_input("Enter Teacher Password:", type="password", on_change=password_entered, key="password")
        st.error("😕 Wrong password. No grades for you today!")
        return False
    else:
        # Password correct
        return True

# If the password is not correct, stop the app here
if not check_password():
    st.stop()

# --- APP CONTINUES ONLY IF AUTHENTICATED ---

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

# --- SIDEBAR: Admin ---
st.sidebar.header("👤 Teacher Account")
st.sidebar.write("Status: **Authenticated** ✅")
if st.sidebar.button("Log Out"):
    del st.session_state["password_correct"]
    st.rerun()

st.sidebar.divider()
new_student = st.sidebar.text_input("Enroll New Student:")
if st.sidebar.button("Add Student"):
    if new_student and new_student not in st.session_state.student_records:
        st.session_state.student_records[new_student] = []
        st.sidebar.success(f"{new_student} added!")

# --- MAIN UI ---
st.title("🎓 Pro Gradebook & Security Dashboard")

# SECTION: ENTRY WITH DATE
st.subheader("📥 Log New Assignment")
col1, col2, col3, col4 = st.columns(4)

with col1:
    target_s = st.selectbox("Student:", list(st.session_state.student_records.keys()))
with col2:
    as_type = st.selectbox("Type:", list(grade_types.keys()))
with col3:
    g_label = st.selectbox("Grade:", list(grade_values.keys()))
with col4:
    # FEATURE: Manual Date Selection
    target_date = st.date_input("Date of Assignment:", value=datetime.now())

if st.button("Commit to Ledger", use_container_width=True):
    val = grade_values[g_label]
    st.session_state.student_records[target_s].append({
        'id': st.session_state.id_counter,
        'value': val,
        'type': as_type,
        'date': target_date.strftime("%Y-%m-%d")
    })
    st.session_state.id_counter += 1
    st.toast(f"Successfully added {val} for {target_s} on {target_date}", icon="📝") #

st.divider()

# --- SECTION: AUDIT LOG & DELETION ---
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
    
    # DELETE BUTTON
    col_del1, col_del2 = st.columns([3, 1])
    with col_del1:
        record_to_del = st.selectbox("Select Record ID to Delete:", options=df["ID"].tolist())
    with col_del2:
        st.write(" ") # Padding
        if st.button("🗑️ Delete Selected", type="primary"):
            for name in st.session_state.student_records:
                st.session_state.student_records[name] = [
                    r for r in st.session_state.student_records[name] if r['id'] != record_to_del
                ]
            st.toast("Entry removed!", icon="🔥")
            st.rerun()
else:
    st.info("Audit log is currently empty.")
