#1
def greet(name, age):
    print(f"My name is {name} and I am {age} years old")

greet("Ali", 18)

#2
def my_function(fname):
  print(fname + " Refsnes")

my_function("Emil")
my_function("Tobias")
my_function("Linus")

#3
def my_function(name): # name is a parameter
  print("Hello", name)

my_function("Emil") # "Emil" is an argument

#4
def my_function(fname, lname):
  print(fname + " " + lname)

my_function("Emil", "Refsnes")