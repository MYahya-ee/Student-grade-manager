class Subject:
    def __init__(self, name, grade):
        self.name = name
        self.grade = float(grade)

    def to_dict(self):      
         return {
              "name":self.name,
              "grade":self.grade
         }