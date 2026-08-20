#GRADEBOOK

import json
from Student import Students
from subject import Subject
from itertools import zip_longest

class GradeBook:
    def __init__(self):
        try:
            with open("students_data.json", "r") as f:
                content = f.read()
            self.students = json.loads(content) if content.strip() else []
        except FileNotFoundError:
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
        with open("students_data.json", "r") as f:
            info = json.load(f)
        print()
        for i in info:    
            if i['grades']:
                for grade in i['grades']: 
                    grades_formatted = " | ".join(f"{g['name']}: {g['grade']}" for g in i['grades'])
            else:
                grades_formatted = "no grades yet"
            print(f"{i['roll_number']} {i['name']:<12} {grades_formatted}")

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
            with open("students_data.json", "r") as f:
                students = json.load(f)
            for student in students:
                if not student['grades']:
                    continue
                total_score = 0
                for grade in student['grades']:
                    total_score += int(grade['grade'])
                percent = (total_score/(len(student['grades'])))
                fin = {'name' : student['name'], 'percent': percent, "roll_number":student['roll_number']}
                perc_list_students.append(fin)
            return perc_list_students

    def view_single(self, roll_number):
        with open("students_data.json", "r") as f:
            info = json.load(f) 
        for i in info:
            if roll_number == i['roll_number']:
                if i['grades']:
                    for grade in i['grades']: 
                        grades_formatted = " | ".join(f"{g['name']}: {g['grade']}" for g in i['grades'])
                else:
                    grades_formatted = "no grades yet"
                print(f"""Name: {i['name']}

    

Roll number: {i['roll_number']}
Grades: {grades_formatted}""")

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

            case "1": #Add a student
                name = input("Enter the name of student: ")
                s1 = Students(name)
                gradebook.add_student(s1.to_dict())
                print(f"\"{s1.name}\" has been added having roll number: {s1.roll_number}")

            case "2": #adding subject and marks
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

            case "3": #view all students
                gradebook.view_all()

            case"4":
                rn = input("Enter the roll number of student: ")
                gradebook.view_single(rn)    

            case "5":
                gradebook.rankings()    

            case "6":
                rollnumber = input("Enter the roll number: ")
                gradebook.pass_fail(rollnumber)
                
main()