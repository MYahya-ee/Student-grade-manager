#GRADEBOOK

import json
from Student import Students
from subject import Subject
from itertools import zip_longest
from datetime import datetime

class GradeBook:
    def __init__(self):
        try:
            with open("students_data.json", "r") as f:
                content = f.read()
            self.students = json.loads(content) if content.strip() else []
        except FileNotFoundError:
            self.students = []
        except json.JSONDecodeError:
            self.students = []

    def add_student(self, student_dict):
        self.students.append(student_dict)
        with open("students_data.json", "w") as f:
            json.dump(self.students, f, indent=2)

    def add_grades(self, roll, sub_name, grade):
        for student in self.students:
            if roll == student["roll_number"]:
                student["grades"].append(Subject(sub_name, grade).to_dict())
        with open("students_data.json", "w") as f:
            json.dump(self.students, f, indent=2)

    def view_all(self):
        percentages = {s['name']: s['percent'] for s in self.get_percentage()}
        print()
        for i in self.students:
            if i['grades']:
                grades_formatted = " | ".join(f"{g['name']}: {g['grade']}" for g in i['grades'])
                percent = f"{percentages.get(i['name'], 0):.2f}%"
            else:
                grades_formatted = "no grades yet"
                percent = "N/A"
            print(f"{i['roll_number']:<6} {i['name']:<12} {percent:<10} {grades_formatted}")

    def rankings(self):
        lis_perc = self.get_percentage()
        ranked = sorted(lis_perc, key=lambda x: x['percent'], reverse=True)
        print()
        for i, student in enumerate(ranked):
            print(f"{i+1}. {student['name']:<12} {student['percent']:.2f}%")

    def pass_fail(self, rollno):
        list_perc = self.get_percentage()
        for student in list_perc:
            if rollno == student['roll_number']:
                if int(student['percent']) < 50:
                    print("Failed")
                else:
                    print(f"Passed with {student['percent']}%")

        inp = input("Do you wanna see who passed and who failed? (Y/N) ").capitalize()
        if inp == "Y":
            failed_students = []
            passed_students = []
            for student in list_perc:
                if int(student['percent']) < 50:
                    failed_students.append(student['name'])
                else:
                    passed_students.append(student['name'])
            print(f"{'Passed students':<30} {'Failed Students'}")
            print("-"*50)
            for f, p in zip_longest(passed_students, failed_students, fillvalue=""):
                print(f"{f:<30} {p}")
        else:
            print("Going back to menue")

    def get_percentage(self):
        perc_list_students = []
        for student in self.students:
            if not student['grades']:
                continue
            total_score = 0
            for grade in student['grades']:
                total_score += int(grade['grade'])
            percent = total_score / len(student['grades'])
            fin = {'name': student['name'], 'percent': percent, 'roll_number': student['roll_number']}
            perc_list_students.append(fin)
        return perc_list_students

    def view_single(self, roll_number):
        for i in self.students:
            if roll_number == i['roll_number']:
                if i['grades']:
                    grades_formatted = " | ".join(f"{g['name']}: {g['grade']}" for g in i['grades'])
                else:
                    grades_formatted = "no grades yet"
                print(f"""Name: {i['name']}
Roll number: {i['roll_number']}
Grades: {grades_formatted}""")

    def delete_student(self, rollnumber):
        final_list = [s for s in self.students if s['roll_number'] != rollnumber]
        self.students = final_list
        with open("students_data.json", "w") as f:
            json.dump(self.students, f, indent=2)

    def result_sheet(self):
            report = ""
            report += f"STUDENT RESULTS SHEET\n"
            report += f"Generated: {datetime.now().strftime('%H:%M %d/%m')}\n"
            report += f"{'='*50}\n\n"
            report += f"Rankings: \n"
            
            lis_perc = self.get_percentage()
            ranked = sorted(lis_perc, key=lambda x: x['percent'], reverse=True)
            print()
            for i, student in enumerate(ranked):
                report += f"{i+1}. {student['name']:<12} {student['percent']:.2f}%\n"
            report += "\n"
            report += f"{'='*50}\n\n"
            report += f"Full results:\n"
            report += f"{'Roll No':<10} {'Name':<12} {'Percentage':<12} {'Grades'}\n"
            report += f"{'='*50}\n"

            percentages = {s['name']: s['percent'] for s in self.get_percentage()}
            print()
            for i in self.students:
                if i['grades']:
                    grades_formatted = " | ".join(f"{g['name']}: {g['grade']}" for g in i['grades'])
                    percent = f"{percentages.get(i['name'], 0):.2f}%"
                else:
                    grades_formatted = "no grades yet"
                    percent = "N/A"
                report += f"{i['roll_number']:<10} {i['name']:<13} {percent:<11} {grades_formatted}\n"
            report += "\n"
            report += f"{'='*50}\n\n"
            list_perc = self.get_percentage()
            failed_students = []
            passed_students = []
            no_grades = [s['name'] for s in self.students if not s['grades']]

            for student in list_perc:
                if student['percent'] < 50:
                    failed_students.append(student['name'])
                else:
                    passed_students.append(student['name'])
            report += f"PASS/FAIL Summary"
            report += f"Passed: {', '.join(passed_students)}\n"
            report += f"Failed: {', '.join(failed_students) or 'None' }\n"
            if no_grades:
                report += f"No grades entered: {', '.join(no_grades)}\n"
            report += "\n"
            report += f"{'='*50}"
            with open("results.txt", "w") as f:
                f.write(report)
            print("Report saved to reults.txt")
def main():
    gradebook = GradeBook()
    while True:
        print("""\nWhat would you like to do:
1.Add a student
2.Add a subject + grade
3.View all students
4.View a single student
5.View rankings
6.Check pass/fail
7.Update a grade
8.Delete a student
9.Export results sheet
0.Exit
""")
        inp = input()
        match inp:
            case "0":
                exit()
            case "1":
                name = input("Enter the name of student: ")
                s1 = Students(name)
                gradebook.add_student(s1.to_dict())
                print(f"\"{s1.name}\" has been added having roll number: {s1.roll_number}")
            case "2":
                roll = input("Enter roll number to add grades: ")
                while True:
                    sub_name = input("Enter the name of subject: ")
                    grade = input("Enter marks (out of 100): ")
                    gradebook.add_grades(roll, sub_name, grade)
                    inp = input("Do you want to add more subjects and grades? (Y/N) ").strip().capitalize()
                    if inp == "Y":
                        continue
                    else:
                        break
            case "3":
                gradebook.view_all()
            case "4":
                rn = input("Enter the roll number of student: ")
                gradebook.view_single(rn)
            case "5":
                gradebook.rankings()
            case "6":
                rollnumber = input("Enter the roll number: ")
                gradebook.pass_fail(rollnumber)
            case "8":
                roll = input("Enter the roll number of student you wanna delete: ")
                gradebook.delete_student(roll)

            case "9":
                gradebook.result_sheet()
main()  