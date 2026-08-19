import json
from Student import Students
from subject import Subject
subjects = ["Maths", "English", "Physics", "Chemistry", "Biology", "Urdu", ]
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
        with open("students_data.json", "r") as f:
            info = json.load(f)
        for student in info:
            print(f"{student['name']} has been added having roll number {student['roll_number']}")
         

    def add_grades(self, roll, sub_name, grade):
        for student in self.students:
            if roll == student["roll_number"]:
                student["grades"].append(Subject(sub_name, grade).to_dict())
                
        with open("students_data.json", "w") as f:
            json.dump(self.students, f, indent=2)
        
    def view_all(self):
        pass

def main():
    #adding students
    name = input("Enter the name of student: ")
    s1 = Students(name)
    gradebook = GradeBook()
    gradebook.add_student(s1.to_dict())
    #adding subject and marks
    roll = input("Enter roll number to add grades: ")

    while True:
            sub_name = input("Enter the name of subject: ")
            grade = input("Enter grade: (out of 100)")
            gradebook.add_grades(roll, sub_name, grade)

            inp = input("Do you want to add more subjects and grades?").strip().capitalize()
            if inp == "Yes":
                 continue
            else:
                 break
    
main()