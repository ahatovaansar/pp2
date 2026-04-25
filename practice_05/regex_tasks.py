
import re

#1 Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s.
pattern = r"ab*"
print(bool(re.fullmatch(pattern, "abbb")))
print(bool(re.fullmatch(pattern, "a")))

#2 Write a Python program that matches a string that has an 'a' followed by two to three 'b'.
pattern = r"ab{2,3}"
print(bool(re.fullmatch(pattern, "abb")))
print(bool(re.fullmatch(pattern, "abbb")))

#3 Write a Python program to find sequences of lowercase letters joined with a underscore.
text = "hello_world test_string abc_def"
print(re.findall(r"[a-z]+_[a-z]+", text))

#4 Write a Python program to find the sequences of one upper case letter followed by lower case letters.
text = "Hello World Python Regex"
print(re.findall(r"[A-Z][a-z]+", text)) 

#5 Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.
pattern = r"a.*b"
print(bool(re.search(pattern, "axxxb"))) 

#6 Write a Python program to replace all occurrences of space, comma, or dot with a colon.
text = "Hello, world. Python regex"
print(re.sub(r"[ ,\.]", ":", text))

#7 Write a python program to convert snake case string to camel case string.
text = "hello_world_python"
camel = re.sub(r"_([a-z])", lambda x: x.group(1).upper(), text)
print(camel) 

#8 Write a Python program to split a string at uppercase letters.
text = "HelloWorldPython"
print(re.split(r"(?=[A-Z])", text)) 

#9 Write a Python program to insert spaces between words starting with capital letters.
text = "HelloWorldPython"
print(re.sub(r"([A-Z])", r" \1", text).strip())

#10 Write a Python program to convert a given camel case string to snake case.
text = "helloWorldPython"
snake = re.sub(r"([A-Z])", r"_\1", text).lower()
print(snake)