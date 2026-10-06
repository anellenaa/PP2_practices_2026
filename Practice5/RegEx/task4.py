# 4. One uppercase letter followed by lowercase letters
import re

text = "Hello World, this Is a Test of PYTHON and Regex"
print(re.findall(r"[A-Z][a-z]+", text))