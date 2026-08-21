# Student Grade Manager

A command-line gradebook system for managing student records, grades, and result reports — built in Python with basic OOP and JSON-based persistence.

## Features

- Add students with auto-generated roll numbers
- Record subject grades per student
- View all students with grades and percentages
- View a single student's full record
- Rank students by overall percentage
- Check pass/fail status (individually or as a full class breakdown)
- Delete a student record
- Export a formatted results sheet to `results.txt`

## Requirements

- Python 3.7+
- No external dependencies — uses only `json`, `uuid`, `itertools`, and `datetime` from the standard library

## Project Structure

```
.
├── Gradebook.py         # Main program and CLI menu
├── Student.py           # Students class
├── subject.py           # Subject class
└── students_data.json   # Auto-generated on first run (student database)
```

## Getting Started

```bash
git clone <your-repo-url>
cd <repo-name>
python Gradebook.py
```

## Usage

Running the program launches a menu:

```
1. Add a student
2. Add a subject + grade
3. View all students
4. View a single student
5. View rankings
6. Check pass/fail
7. Update a grade
8. Delete a student
9. Export results sheet
0. Exit
```

Student data is stored in `students_data.json` and persists between sessions. A student passes with an average of 50% or higher across all recorded subject grades.

## Known Issues

- Option 7 (Update a grade) is listed in the menu but has no handler yet — selecting it currently does nothing.

## License

MIT
