# 5. 'a' followed by anything, ending in 'b'
import re

def match(s):
    return bool(re.fullmatch(r"a.*b", s))

for s in ["ab", "a123b", "acb", "a b", "abc", "ba"]:
    print(f"{s!r}: {match(s)}")