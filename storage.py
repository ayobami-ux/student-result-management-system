import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "students.json"


def load_students():
    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not DATA_FILE.exists():
            return []
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read the data file. Starting with an empty list.")
        return []


def save_students(students):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)
