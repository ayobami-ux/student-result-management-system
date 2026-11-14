import streamlit as st
from student import Student
from storage import load_students, save_students
from results import calculate_result
from reports import students_with_results
from datetime import datetime

st.set_page_config(page_title="Student Result Management System", page_icon="🎓", layout="wide")
st.title("🎓 Student Result Management System")
st.caption("Register students, manage scores and view academic results.")

if "students" not in st.session_state:
    st.session_state.students = load_students()
students = st.session_state.students
subjects = ["English", "Mathematics", "Biology", "Chemistry", "Physics"]

def find_student(student_id):
    for item in students:
        if item["student_id"].lower() == student_id.lower():
            return item
    return None

def persist():
    save_students(students)

tab1, tab2, tab3, tab4 = st.tabs([
    "Register student", "Enter scores", "Student report", "Class results"
])

with tab1:
    st.subheader("Register a new student")
    with st.form("register_form", clear_on_submit=True):
        student_id = st.text_input("Student ID")
        full_name = st.text_input("Full name")
        class_form = st.text_input("Class/Form")
        gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
        dob = st.date_input("Date of birth")
        submitted = st.form_submit_button("Register student")
    if submitted:
        if not all([student_id.strip(), full_name.strip(), class_form.strip()]) or gender == "Select":
            st.error("Please complete all fields.")
        elif find_student(student_id.strip()):
            st.error("A student with this ID already exists.")
        else:
            record = Student(student_id.strip(), full_name.strip(), class_form.strip(),
                             gender, dob.strftime("%d/%m/%Y"))
            students.append(record.to_dict())
            persist()
            st.success(f"{full_name} was successfully registered!")

with tab2:
    st.subheader("Enter or update scores")
    if not students:
        st.info("Register a student first.")
    else:
        chosen_id = st.selectbox(
            "Select student", [s["student_id"] for s in students],
            format_func=lambda sid: f'{sid} — {find_student(sid)["full_name"]}'
        )
        chosen = find_student(chosen_id)
        existing = chosen.get("scores", {})
        with st.form("scores_form"):
            entered = {}
            cols = st.columns(2)
            for i, subject in enumerate(subjects):
                with cols[i % 2]:
                    entered[subject] = st.number_input(
                        f"{subject} score", min_value=0.0, max_value=100.0,
                        value=float(existing.get(subject, 0.0)), step=1.0
                    )
            score_submit = st.form_submit_button("Save scores")
        if score_submit:
            chosen["scores"] = entered
            chosen["date_entered"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            persist()
            st.success("Scores saved successfully!")

with tab3:
    st.subheader("Individual student report")
    if not students:
        st.info("No students have been registered.")
    else:
        report_id = st.selectbox(
            "Choose student", [s["student_id"] for s in students], key="report_id",
            format_func=lambda sid: f'{sid} — {find_student(sid)["full_name"]}'
        )
        report_student = find_student(report_id)
        st.write(f'**Name:** {report_student["full_name"]}')
        st.write(f'**Class/Form:** {report_student["class_form"]}')
        scores = report_student.get("scores", {})
        if len(scores) >= 5:
            result = calculate_result(scores)
            st.dataframe([{"Subject": k, "Score": v} for k, v in scores.items()],
                         use_container_width=True)
            c1, c2, c3 = st.columns(3)
            c1.metric("Total", f'{result["total"]:.1f}')
            c2.metric("Average", f'{result["average"]:.2f}')
            c3.metric("Grade", result["grade"])
            st.caption(f'Last entered: {report_student.get("date_entered", "Not recorded")}')
        else:
            st.warning("Scores have not been entered for all five subjects.")

with tab4:
    st.subheader("Class results and statistics")
    completed = students_with_results(students)
    if not completed:
        st.info("No complete results are available yet.")
    else:
        completed.sort(key=lambda x: x["average"], reverse=True)
        st.dataframe([{
            "Student ID": x["student"]["student_id"],
            "Name": x["student"]["full_name"],
            "Total": x["total"],
            "Average": round(x["average"], 2),
            "Grade": x["grade"]
        } for x in completed], use_container_width=True)
        averages = [x["average"] for x in completed]
        c1, c2, c3 = st.columns(3)
        c1.metric("Highest average", f"{max(averages):.2f}")
        c2.metric("Lowest average", f"{min(averages):.2f}")
        c3.metric("Class average", f"{sum(averages) / len(averages):.2f}")

with st.sidebar:
    st.header("Student records")
    st.write(f"Registered students: **{len(students)}**")
    if st.button("Refresh records"):
        st.session_state.students = load_students()
        st.rerun()
    st.caption("Grade scale: A ≥ 70, B ≥ 60, C ≥ 50, D ≥ 45, F < 45.")
