from functools import reduce

numbers = [1, 2, 3, 4, 5]

# map example
squares = list(map(lambda x: x * x, numbers))
print("Squares:", squares)

# filter example
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even_numbers)

# reduce example
total = reduce(lambda a, b: a + b, numbers)
print("Sum:", total)