def calculate_result(scores):
    total = sum(scores.values())
    average = total / len(scores) if scores else 0

    if average >= 70:
        grade = "A"
    elif average >= 60:
        grade = "B"
    elif average >= 50:
        grade = "C"
    elif average >= 45:
        grade = "D"
    else:
        grade = "F"

    return {"total": total, "average": average, "grade": grade}
