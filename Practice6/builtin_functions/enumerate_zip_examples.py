"""Practice 6 - enumerate(), zip(), type checking and conversions."""

names = ["Ali", "Aigerim", "Dana"]
scores = [90, 85, 77]
cities = ["Almaty", "Astana", "Shymkent"]

# 3. enumerate(): index + value
for i, name in enumerate(names, start=1):
    print(i, name)

# zip(): paired iteration
for name, score in zip(names, scores):
    print(f"{name}: {score}")

for name, score, city in zip(names, scores, cities):
    print(name, score, city)

# zip -> dict, and unzip
print(dict(zip(names, scores)))
pairs = list(zip(names, scores))
n, s = zip(*pairs)
print("unzipped:", n, s)

# enumerate + zip together
for i, (name, score) in enumerate(zip(names, scores)):
    print(i, name, score)

# 4. Type checking and conversions
values = [10, 3.14, "42", True, [1, 2], (1, 2), {"a": 1}, {1, 2}, None]
for v in values:
    print(repr(v), "->", type(v).__name__, "| is int:", isinstance(v, int))

print(int("42") + 1)          # str -> int
print(float("3.5") * 2)       # str -> float
print(str(100) + " points")   # int -> str
print(list("abc"))            # str -> list
print(tuple([1, 2, 3]))       # list -> tuple
print(set([1, 1, 2, 3]))      # list -> set
print(bool(0), bool("hi"))    # -> bool
print(int(7.9), round(7.9))   # float -> int (truncates) vs round

try:
    int("abc")
except ValueError as e:
    print("Conversion error:", e)
