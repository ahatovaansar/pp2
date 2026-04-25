#1
i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1

#2
attempts = 0

while attempts < 3:
    password = input("Enter password: ")
    if password == "admin":
        print("Access granted")
        break
    attempts += 1

