#1
x = lambda a : a + 10
print(x(5))

#2
x = lambda a, b : a * b
print(x(5, 6))

#3
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)

print(mydoubler(11))

#4
def square(x):
    return x * x

# Lambda версия
square_lambda = lambda x: x * x

print(square_lambda(5))
