import uuid
import json
class Students:
    
    def __init__(self, name):
        self.name = name
        self.roll_number = str(uuid.uuid1())[:4]
        self.grades = []
    def to_dict(self):             
        return {
            "name" : self.name,
            "roll_number" : self.roll_number,
            "grades" : self.grades
            
        }

    
