#1
class Student(Person):
  def __init__(self, fname, lname):
    super().__init__(fname, lname)

#2
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, id):
        super().__init__(name)
        self.id = id

s = Student("Ali", 123)
print(s.name, s.id)
