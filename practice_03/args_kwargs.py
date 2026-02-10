#1
def my_function(title, *args, **kwargs):
  print("Title:", title)
  print("Positional arguments:", args)
  print("Keyword arguments:", kwargs)

my_function("User Info", "Emil", "Tobias", age = 25, city = "Oslo")

#2
# *args — любое количество аргументов
def sum_all(*numbers):
    return sum(numbers)

print(sum_all(1, 2, 3, 4))

# **kwargs — именованные аргументы
def print_info(**info):
    for key, value in info.items():
        print(key, ":", value)

print_info(name="Dana", age=19, city="Almaty")

#3
def my_function(username, **details):
  print("Username:", username)
  print("Additional details:")
  for key, value in details.items():
    print(" ", key + ":", value)

my_function("emil123", age = 25, city = "Oslo", hobby = "coding")

#4
def my_function(*numbers):
  total = 0
  for num in numbers:
    total += num
  return total

print(my_function(1, 2, 3))
print(my_function(10, 20, 30, 40))
print(my_function(5))