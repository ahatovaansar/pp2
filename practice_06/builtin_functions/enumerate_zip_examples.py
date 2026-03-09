names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

# enumerate
for i, name in enumerate(names):
    print(i, name)

# zip
for name, score in zip(names, scores):
    print(name, score)

# sorted
numbers = [5, 2, 9, 1]
print(sorted(numbers))