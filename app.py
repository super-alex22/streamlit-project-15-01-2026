import streamlit as st
import pandas as pd

# 1. The "Grand Opening" of our app
st.title("🍎 Class Performance - The Wall of Fame (and Shame)")

# 2. Memory Lane: Initializing session state so our data doesn't disappear 
# like a student's motivation on a Friday afternoon.
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

st.subheader("📝 Enter Student Progress")

# 3. User Input: Let the teacher pick their "victim" and their grade
student = st.selectbox("Select Student:", list(st.session_state.students.keys()))
grade = st.selectbox("Select Grade Level:", list(st.session_state.grades.keys()))

# 4. The Magic Button: Saving the data
if st.button("Save Record"):
    st.session_state.students[student] += 1
    st.session_state.grades[grade] += 1
    st.success(f"Record saved! {student} now has one more {grade} on their permanent record.")

st.divider()

st.subheader("📊 Analytics (The Truth Hurts)")

# 5. Visualizing: Creating the tables and charts
# Students Chart
st.write("Activity per Student")
students_df = pd.DataFrame.from_dict(
    st.session_state.students, orient="index", columns=["Entries"]
)
st.bar_chart(students_df)

# Grades Chart
st.write("Grade Distribution")
grades_df = pd.DataFrame.from_dict(
    st.session_state.grades, orient="index", columns=["Total"]
)
st.bar_chart(grades_df)
