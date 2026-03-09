import shutil
import os

# copy file
shutil.copy("example.txt", "backup.txt")
print("File copied")

# delete file
if os.path.exists("backup.txt"):
    os.remove("backup.txt")
    print("Backup deleted")