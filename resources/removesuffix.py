import os

suffix = "_french"

for folder in os.walk("."):
    for filename in folder[2]:
        if suffix in filename:
            filename = os.path.join(folder[0], filename)
            print filename
            os.rename(filename, filename.replace(suffix, ""))