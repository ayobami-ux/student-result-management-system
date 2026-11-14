# Student Result Management System

A simple command-line Student Result Management System built with Python.

## Features
- Register, view, search, update and delete students.
- Enter or update scores for five subjects.
- Calculate total, average and grade automatically.
- Display individual report cards.
- Sort results by average (highest to lowest).
- Display class statistics.
- Save a text report.
- Store student records in a JSON file and load them when the program starts.

## Requirements
- Python 3 installed.
- No external packages are required.

## How to Run
1. Download or clone this repository.
2. Open the project folder in VS Code.
3. Open the terminal in VS Code.
4. Run:

   ```bash
   python main.py
   ```

5. Follow the menu displayed in the terminal.

## Grade Scale
- A: 70–100
- B: 60–69
- C: 50–59
- D: 45–49
- F: Below 45

## Project Files
- `main.py`: Main menu and program operations.
- `student.py`: Student class.
- `results.py`: Total, average and grade calculations.
- `storage.py`: JSON file loading and saving.
- `reports.py`: Result lists, statistics and text report.
- `data/students.json`: Stored student records.
