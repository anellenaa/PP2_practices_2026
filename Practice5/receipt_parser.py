# Examples for every re function, flags, metacharacters, special sequences, quantifiers
import re

text = "The rain in Spain stays mainly in the plain"

print("--- re.search (first match anywhere) ---")
m = re.search(r"ai", text)
print(m.group(), m.start(), m.end(), m.span())

print("--- re.match (only at the beginning) ---")
print(re.match(r"The", text))        # match
print(re.match(r"rain", text))       # None

print("--- re.fullmatch (whole string) ---")
print(re.fullmatch(r"\d+", "12345"))

print("--- re.findall (all matches) ---")
print(re.findall(r"ai", text))

print("--- re.finditer ---")
for m in re.finditer(r"\bS\w+", text):
    print(m.group(), m.span())

print("--- re.split ---")
print(re.split(r"\s", text))
print(re.split(r"\s", text, 2))      # maxsplit=2

print("--- re.sub (replace) ---")
print(re.sub(r"\s", "_", text))
print(re.sub(r"\s", "_", text, 2))   # count=2

print("--- Metacharacters ---")
print(re.findall(r"r.in", text))              # .  any char
print(re.findall(r"^The", text))              # ^  starts with
print(re.findall(r"plain$", text))            # $  ends with
print(re.findall(r"ai*n", text))              # *  0 or more
print(re.findall(r"ai+n", text))              # +  1 or more
print(re.findall(r"ai?n", text))              # ?  0 or 1
print(re.findall(r"[aeiou]", text))           # [] set
print(re.findall(r"Spain|plain", text))       # |  or
print(re.findall(r"(ai)(n)", text))           # () group
print(re.findall(r"\.", "a.b.c"))             # \  escape

print("--- Special sequences ---")
s = "Order 66, item_A7 costs $40"
print(re.findall(r"\d", s))      # digits
print(re.findall(r"\D+", s))     # non-digits
print(re.findall(r"\w+", s))     # word chars
print(re.findall(r"\W", s))      # non-word chars
print(re.findall(r"\s", s))      # whitespace
print(re.findall(r"\S+", s))     # non-whitespace
print(re.findall(r"\AOrder", s)) # \A start of string
print(re.findall(r"\$40\Z", s))  # \Z end of string
print(re.findall(r"\bitem", s))  # \b word boundary

print("--- Sets ---")
print(re.findall(r"[a-n]", "arnold"))
print(re.findall(r"[^abc]", "abcxyz"))
print(re.findall(r"[0-9][0-9]", "12 345"))

print("--- Quantifiers ---")
print(re.findall(r"o{2}", "foo fooo fo"))
print(re.findall(r"o{2,}", "foo fooo fo"))
print(re.findall(r"o{1,2}", "foo fooo fo"))

print("--- Flags ---")
print(re.findall(r"spain", text, re.IGNORECASE))
print(re.findall(r"^\w+", "one\ntwo\nthree", re.MULTILINE))
print(re.findall(r"a.b", "a\nb", re.DOTALL))