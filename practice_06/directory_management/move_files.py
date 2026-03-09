import shutil

# move file
shutil.move("example.txt", "test_folder/example.txt")

# copy file back
shutil.copy("test_folder/example.txt", "copy_example.txt")

print("Move and copy done")