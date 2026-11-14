from student import Student
from storage import load_students, save_students
from results import calculate_result
from reports import display_all_results, show_statistics, save_text_report


def get_student(students, student_id):
    for student in students:
        if student["student_id"].lower() == student_id.lower():
            return student
    return None


def add_student(students):
    print("\n--- Register Student ---")
    student_id = input("Student ID: ").strip()
    if not student_id:
        print("Student ID cannot be empty.")
        return
    if get_student(students, student_id):
        print("A student with that ID already exists.")
        return

    name = input("Full name: ").strip()
    class_form = input("Class/Form: ").strip()
    gender = input("Gender: ").strip()
    dob = input("Date of birth (DD/MM/YYYY): ").strip()

    if not all([name, class_form, gender, dob]):
        print("Please fill in all the fields.")
        return

    student = Student(student_id, name, class_form, gender, dob)
    students.append(student.to_dict())
    save_students(students)
    print("Student registered successfully.")


def view_students(students):
    if not students:
        print("\nNo students have been registered.")
        return
    print("\n--- Registered Students ---")
    for student in students:
        print(f'{student["student_id"]} | {student["full_name"]} | '
              f'{student["class_form"]} | {student["gender"]} | {student["date_of_birth"]}')


def search_student(students):
    term = input("\nEnter student ID or name: ").strip().lower()
    matches = [s for s in students if term in s["student_id"].lower()
               or term in s["full_name"].lower()]
    if not matches:
        print("No matching student found.")
        return
    for s in matches:
        print(f'{s["student_id"]} | {s["full_name"]} | {s["class_form"]}')


def update_student(students):
    student = get_student(students, input("\nEnter student ID to update: ").strip())
    if not student:
        print("Student not found.")
        return
    print("Press Enter to keep the current value.")
    for key, label in [
        ("full_name", "Full name"),
        ("class_form", "Class/Form"),
        ("gender", "Gender"),
        ("date_of_birth", "Date of birth")
    ]:
        new_value = input(f'{label} [{student[key]}]: ').strip()
        if new_value:
            student[key] = new_value
    save_students(students)
    print("Student information updated.")


def delete_student(students):
    student = get_student(students, input("\nEnter student ID to delete: ").strip())
    if not student:
        print("Student not found.")
        return
    confirm = input(f'Delete {student["full_name"]}? (y/n): ').strip().lower()
    if confirm == "y":
        students.remove(student)
        save_students(students)
        print("Student record deleted.")


def enter_scores(students):
    student = get_student(students, input("\nEnter student ID: ").strip())
    if not student:
        print("Student not found.")
        return

    print("Enter scores from 0 to 100.")
    subjects = ["English", "Mathematics", "Biology", "Chemistry", "Physics"]
    scores = {}
    for subject in subjects:
        while True:
            try:
                score = float(input(f"{subject}: "))
                if 0 <= score <= 100:
                    scores[subject] = score
                    break
                print("Score must be between 0 and 100.")
            except ValueError:
                print("Please enter a valid number.")

    student["scores"] = scores
    student["date_entered"] = __import__("datetime").datetime.now().strftime("%d/%m/%Y %H:%M")
    save_students(students)
    print("Scores saved successfully.")


def show_report_card(students):
    student = get_student(students, input("\nEnter student ID: ").strip())
    if not student:
        print("Student not found.")
        return
    if len(student.get("scores", {})) < 5:
        print("This student does not have scores for five subjects yet.")
        return
    result = calculate_result(student["scores"])
    print("\n========== STUDENT REPORT CARD ==========")
    print("Student:", student["full_name"])
    print("Student ID:", student["student_id"])
    print("Class/Form:", student["class_form"])
    print("------------------------------------------")
    for subject, score in student["scores"].items():
        print(f"{subject:<18} {score:>6.1f}")
    print("------------------------------------------")
    print("Total:", result["total"])
    print("Average:", f'{result["average"]:.2f}')
    print("Grade:", result["grade"])
    print("Date entered:", student.get("date_entered", "Not recorded"))
    print("==========================================")


def main():
    students = load_students()
    while True:
        print("""
========== STUDENT RESULT MANAGEMENT SYSTEM ==========
1. Register a student
2. View all students
3. Search for a student
4. Update student information
5. Delete a student
6. Enter or update student scores
7. View individual report card
8. View all results
9. Show class statistics
10. Save text report
0. Exit
======================================================
""")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            enter_scores(students)
        elif choice == "7":
            show_report_card(students)
        elif choice == "8":
            display_all_results(students)
        elif choice == "9":
            show_statistics(students)
        elif choice == "10":
            save_text_report(students)
        elif choice == "0":
            save_students(students)
            print("Thank you for using the system.")
            break
        else:
            print("Invalid option. Please choose from the menu.")


if __name__ == "__main__":
    main()
