# 1. 'a' followed by zero or more 'b'
import re

def match(s):
    return bool(re.fullmatch(r"ab*", s))

for s in ["a", "ab", "abbb", "b", "ac", "abc"]:
    print(f"{s!r}: {match(s)}")