# 9. Insert spaces between words starting with capital letters
import re

text = "InsertSpacesBetweenWords"
print(re.sub(r"(?<!^)(?=[A-Z])", " ", text))   # Insert Spaces Between Words