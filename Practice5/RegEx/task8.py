# 8. Split a string at uppercase letters
import re

text = "SplitAtUppercaseLetters"
print(re.split(r"(?=[A-Z])", text))
# In Python 3.7+ an empty first element can appear for strings starting with a capital:
print([p for p in re.split(r"(?=[A-Z])", text) if p])