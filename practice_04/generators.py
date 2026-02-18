#1 Iterator
mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))

#2
numbers = [1, 2, 3, 4, 5]

my_iter = iter(numbers)

print("Iterator example:")
print(next(my_iter))
print(next(my_iter))
print(next(my_iter))

#3
def my_generator():
  yield 1
  yield 2
  yield 3

for value in my_generator():
  print(value)