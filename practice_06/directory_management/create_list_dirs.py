import os

# create folder
os.mkdir("test_folder")

# create nested folders
os.makedirs("parent/child/grandchild", exist_ok=True)

# show files in folder
print(os.listdir())

# current directory
print(os.getcwd())