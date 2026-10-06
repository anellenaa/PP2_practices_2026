# 3. Sequences of lowercase letters joined with an underscore
import re

text = "hello_world, my_var_name, Hello_World, abc, a_b"
print(re.findall(r"\b[a-z]+(?:_[a-z]+)+\b", text))