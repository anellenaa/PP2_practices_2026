# 2. 'a' followed by two to three 'b'
import re

def match(s):
    return bool(re.fullmatch(r"ab{2,3}", s))

for s in ["a", "ab", "abb", "abbb", "abbbb"]:
    print(f"{s!r}: {match(s)}")