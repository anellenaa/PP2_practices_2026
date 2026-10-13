"""Practice 6 - map(), filter(), reduce() and other built-ins."""
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# basic built-ins: len, sum, min, max, sorted
print("len   :", len(numbers))
print("sum   :", sum(numbers))
print("min   :", min(numbers))
print("max   :", max(numbers))
print("sorted desc:", sorted(numbers, reverse=True))

# 1. map() and filter() on lists
squares = list(map(lambda x: x ** 2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("squares:", squares)
print("evens  :", evens)

words = ["python", "file", "path", "os"]
print("upper  :", list(map(str.upper, words)))
print("len>3  :", list(filter(lambda w: len(w) > 3, words)))

# 2. reduce() from functools
total = reduce(lambda a, b: a + b, numbers)
product = reduce(lambda a, b: a * b, numbers)
biggest = reduce(lambda a, b: a if a > b else b, numbers)
print("reduce sum    :", total)
print("reduce product:", product)
print("reduce max    :", biggest)
