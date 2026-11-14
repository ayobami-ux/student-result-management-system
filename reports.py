from results import calculate_result


def students_with_results(students):
    result_list = []
    for student in students:
        scores = student.get("scores", {})
        if len(scores) >= 5:
            result = calculate_result(scores)
            result_list.append({
                "student": student,
                "total": result["total"],
                "average": result["average"],
                "grade": result["grade"]
            })
    return result_list


def display_all_results(students):
    results = students_with_results(students)
    if not results:
        print("\nNo complete student results are available.")
        return

    print("\n--- All Student Results ---")
    print(f'{"ID":<12} {"NAME":<25} {"TOTAL":>8} {"AVERAGE":>10} {"GRADE":>7}')
    for item in sorted(results, key=lambda x: x["average"], reverse=True):
        student = item["student"]
        print(f'{student["student_id"]:<12} {student["full_name"]:<25} '
              f'{item["total"]:>8.1f} {item["average"]:>10.2f} {item["grade"]:>7}')


def show_statistics(students):
    results = students_with_results(students)
    if not results:
        print("\nThere are no complete results to analyse.")
        return

    averages = [item["average"] for item in results]
    print("\n--- Class Statistics ---")
    print("Students with complete results:", len(results))
    print("Highest average:", f"{max(averages):.2f}")
    print("Lowest average:", f"{min(averages):.2f}")
    print("Class average:", f"{sum(averages) / len(averages):.2f}")


def save_text_report(students):
    results = students_with_results(students)
    results.sort(key=lambda x: x["average"], reverse=True)
    report_file = "student_results_report.txt"

    with open(report_file, "w", encoding="utf-8") as file:
        file.write("STUDENT RESULT MANAGEMENT SYSTEM\n")
        file.write("=" * 45 + "\n")
        for item in results:
            student = item["student"]
            file.write(
                f'{student["student_id"]} | {student["full_name"]} | '
                f'Total: {item["total"]:.1f} | Average: {item["average"]:.2f} | '
                f'Grade: {item["grade"]}\n'
            )

    print(f"Text report saved as {report_file}.")
