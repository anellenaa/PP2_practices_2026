# 6. Replace all spaces, commas, dots with a colon
import re

text = "Python, Java. C++ and Go"
print(re.sub(r"[ ,.]", ":", text))