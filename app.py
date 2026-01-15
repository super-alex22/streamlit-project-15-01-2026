import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Class Manager Pro", page_icon="📝")

# 2. Data Initialization (Session State)
# Ensures data persists during the user session
if "students" not in st.session_state:
    st.session_state.students = {
        "Ivan": 0,
        "Maria": 0,
        "Georgi": 0,
        "Elena": 0
    }

if "grades" not in st.session_state:
    st.session_state.grades = {
        "Excellent (6)": 0,
        "Very Good (5)": 0,
        "Good (4)": 0,
        "Satisfactory (3)": 0,
        "Poor (2)": 0
    }

# --- SIDEBAR: Management Tools ---
st.sidebar.header("⚙️ Administration")

# Feature: Add new students to the list
new_student_name = st.sidebar.text_input("Enroll a new student:")
if st.sidebar.button("Add to Roster"):
    if new_student_name and new_student_name not in st.session_state.students:
        st.session_state.students[new_student_name] = 0
        st.sidebar.success(f"{new_student_name} added!")
    else:
        st.sidebar.error("Invalid name or student exists.")

st.sidebar.divider()

# Feature: Emergency Reset
if st.sidebar.button("🔥 Reset All Data", help="Wipes all counts and stats"):
    st.session_state.students = {k: 0 for k in st.session_state.students}
    st.session_state.grades = {k: 0 for k in st.session_state.grades}
    st.rerun()

# --- MAIN INTERFACE ---
st.title("🎓 Smart Gradebook Dashboard")
st.write("Manage student performance and track grade distribution in real-time.")

# Organizing layout into columns
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📥 Data Entry")
    selected_student = st.selectbox("Select Student:", list(st.session_state.students.keys()))
    selected_grade = st.selectbox("Assign Grade:", list(st.session_state.grades.keys()))

    if st.button("Submit Record", use_container_width=True):
        st.session_state.students[selected_student] += 1
        st.session_state.grades[selected_grade] += 1
        
        # Celebration for top grades
        if "6" in selected_grade:
            st.balloons()
            st.success(f"Great job, {selected_student}!")
        else:
            st.info("Record updated successfully.")

with col2:
    st.subheader("💾 Export")
    # Generating CSV for download
    df_report = pd.DataFrame.from_dict(st.session_state.students, orient="index", columns=["Entries"])
    csv_data = df_report.to_csv().encode('utf-8')
    
    st.download_button(
        label="Download Report",
        data=csv_data,
        file_name='student_activity.csv',
        mime='text/csv',
        use_container_width=True
    )

st.divider()

# --- VISUALIZATION SECTION ---
st.header("📊 Performance Analytics")

# Using tabs to separate different charts
tab_students, tab_grades = st.tabs(["Student Activity", "Grade Stats"])

with tab_students:
    st.write("Total entries per student:")
    chart_data_students = pd.DataFrame.from_dict(st.session_state.students, orient="index", columns=["Count"])
    st.bar_chart(chart_data_students)

with tab_grades:
    st.write("Frequency of awarded grades:")
    chart_data_grades = pd.DataFrame.from_dict(st.session_state.grades, orient="index", columns=["Total"])
    st.bar_chart(chart_data_grades)

st.caption("System Online. Ready for inputs.")
