#1
x = 10
y = 5

print(x > 5 and y < 10)   # True
print(x > 5 and y > 10)   # False

#2
age = 20
has_id = True

print(age >= 18 and has_id)     # True
print(age < 18 or has_id)       # True
print(not (age < 18))           # True

#3
temperature = 30

if temperature > 25 and temperature < 40:
    print("Temperature is in a safe range")
