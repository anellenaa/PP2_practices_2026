# Iterators and generators


# 1. Generator of squares of numbers up to N
def squares_up_to(N):
    for i in range(N + 1):
        yield i ** 2


# 2. Even numbers from 0 to n
def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i


# 3. Numbers divisible by both 3 and 4 in the range 0..n
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


# 4. Squares of all numbers from a to b
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2


# 5. Numbers from n down to 0
def countdown(n):
    while n >= 0:
        yield n
        n -= 1


if __name__ == "__main__":
    N = 5
    print("1.", list(squares_up_to(N)))

    n = int(input("2. Enter n: "))
    print(",".join(str(x) for x in even_numbers(n)))

    n = int(input("3. Enter n: "))
    print(list(divisible_by_3_and_4(n)))

    print("4.")
    for value in squares(3, 7):
        print(value)

    print("5.", list(countdown(5)))