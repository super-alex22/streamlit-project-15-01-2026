import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Pro Gradebook: Final Formation", page_icon="⚖️", layout="wide")

# 2. Authentication System
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
        "Ivan": [{'id': 1, 'value': 6, 'type': 'Final Exam', 'date': '2026-01-10'}],
        "Maria": [{'id': 2, 'value': 5, 'type': 'Test', 'date': '2026-01-12'}]
    }

if "manual_overrides" not in st.session_state:
    # Stores { "StudentName": {"grade": 6, "reason": "Consistent improvement"} }
    st.session_state.manual_overrides = {}

if "id_counter" not in st.session_state:
    st.session_state.id_counter = 3

# Weights from our previous agreement
grade_types = {
    "Active Participation": 0.5, "Homework": 1.0, "Oral Test": 1.5,
    "Test": 2.0, "Project": 2.0, "Control Work": 2.5, "Final Exam": 3.0
}

grade_values = {
    "Excellent (6)": 6, "Very Good (5)": 5, "Good (4)": 4, 
    "Satisfactory (3)": 3, "Poor (2)": 2
}

# --- DIALOGS (Confirmations) ---

@st.dialog("Confirm Manual Grade Override")
def confirm_override_dialog(student, old_grade, new_grade, reason):
    st.warning("⚠️ You are choosing to bypass the mathematical calculation!")
    st.write(f"**Student:** {student}")
    st.write(f"**Math Grade:** {old_grade} ➡️ **New Final Grade:** {new_grade}")
    st.write(f"**Reason:** {reason}")
    
    if st.button("Confirm Override", type="primary", use_container_width=True):
        st.session_state.manual_overrides[student] = {
            "grade": new_grade,
            "reason": reason
        }
        st.toast(f"Override applied for {student}!", icon="⚖️")
        st.rerun()

@st.dialog("Confirm Grade Addition")
def confirm_add_dialog(student, grade_label, category, date):
    st.write(f"Add **{grade_label}** to **{student}** for **{category}**?")
    if st.button("Confirm Entry", use_container_width=True):
        val = grade_values[grade_label]
        st.session_state.student_records[student].append({
            'id': st.session_state.id_counter,
            'value': val,
            'type': category,
            'date': date.strftime("%Y-%m-%d")
        })
        st.session_state.id_counter += 1
        st.toast("Grade added!", icon="📝")
        if val == 6: st.balloons()
        st.rerun()

# --- HELPER LOGIC ---
def get_weighted_gpa(records):
    if not records: return 0.0
    total_score = sum(r['value'] * grade_types[r['type']] for r in records)
    total_weight = sum(grade_types[r['type']] for r in records)
    return round(total_score / total_weight, 2)

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Administration")
    new_student = st.text_input("Enroll Student:")
    if st.button("Add to Roster"):
        if new_student and new_student not in st.session_state.student_records:
            st.session_state.student_records[new_student] = []
            st.success(f"{new_student} added!")
    
    st.divider()
    if st.button("Logout"):
        del st.session_state["password_correct"]
        st.rerun()

# --- MAIN UI ---
st.title("🛡️ The Unstoppable Gradebook Pro")

# 1. Entry Section
st.subheader("📥 Add New Performance Entry")
c1, c2, c3, c4 = st.columns(4)
with c1: s_target = st.selectbox("Student:", list(st.session_state.student_records.keys()))
with c2: g_type = st.selectbox("Type:", list(grade_types.keys()))
with c3: g_label = st.selectbox("Grade:", list(grade_values.keys()))
with c4: g_date = st.date_input("Date:", value=datetime.now())

if st.button("Log Grade", use_container_width=True):
    confirm_add_dialog(s_target, g_label, g_type, g_date)

st.divider()

# 2. Final Formation & Overrides
st.header("📊 Final Grade Formation")

report_rows = []
for name, records in st.session_state.student_records.items():
    raw_avg = get_weighted_gpa(records)
    math_grade = int(raw_avg + 0.5) if raw_avg > 0 else 0
    
    # Check for manual override
    override = st.session_state.manual_overrides.get(name)
    final_grade = override["grade"] if override else math_grade
    method = "✍️ Manual" if override else "🤖 Math"
    reason = override["reason"] if override else "As calculated"
    
    report_rows.append({
        "Student": name,
        "Math GPA": raw_avg,
        "Calculated": math_grade,
        "Final Grade": final_grade,
        "Method": method,
        "Reasoning": reason
    })

df_report = pd.DataFrame(report_rows)
st.dataframe(df_report, use_container_width=True, hide_index=True)

# 3. Manual Override Section
with st.expander("🛠️ Manual Grade Override Tool"):
    st.write("Use this to adjust the final grade based on your professional judgment.")
    ov_student = st.selectbox("Select Student to Override:", list(st.session_state.student_records.keys()), key="ov_select")
    
    # Show current math result
    ov_avg = get_weighted_gpa(st.session_state.student_records[ov_student])
    ov_math = int(ov_avg + 0.5) if ov_avg > 0 else 0
    st.info(f"Mathematical Grade for {ov_student}: **{ov_math}**")
    
    col_ov1, col_ov2 = st.columns(2)
    with col_ov1:
        new_f_grade = st.slider("Select New Final Grade:", 2, 6, value=ov_math)
    with col_ov2:
        ov_reason = st.text_input("Reason for Override:", placeholder="e.g., Improved significantly in last month")
    
    if st.button("Apply Override", type="primary"):
        if not ov_reason:
            st.error("Please provide a reason for the manual override!")
        else:
            confirm_override_dialog(ov_student, ov_math, new_f_grade, ov_reason)

if st.session_state.manual_overrides:
    if st.button("Reset All Manual Overrides"):
        st.session_state.manual_overrides = {}
        st.rerun()

st.divider()

# 4. Global Audit Log
st.header("📜 Global Audit Log")
all_entries = []
for name, records in st.session_state.student_records.items():
    for r in records:
        all_entries.append({
            "ID": r['id'], "Date": r['date'], "Student": name, 
            "Category": r['type'], "Score": r['value']
        })

if all_entries:
    df_audit = pd.DataFrame(all_entries).sort_values(by="Date", ascending=False)
    st.dataframe(df_audit, use_container_width=True, hide_index=True)
    
    record_to_del = st.selectbox("Select ID to remove:", options=df_audit["ID"].tolist())
    if st.button("🗑️ Delete Selected Entry", type="secondary"):
        confirm_delete_dialog(record_to_del)
