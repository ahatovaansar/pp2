#1
class Student:
    university = "KBTU"   # class variable

    def __init__(self, name):
        self.name = name  # instance variable

s1 = Student("Ali")
s2 = Student("Dana")

print(s1.university)
print(s2.name)
