#1
class Animal:
    def speak(self):
        print("Animal makes a sound")

class Dog(Animal):
    pass

dog = Dog()
dog.speak()

#2
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#Use the Person class to create an object, and then execute the printname method:

x = Person("John", "Doe")
x.printname()