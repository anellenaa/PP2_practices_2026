# Here is a function that returns a single calculated value
def multiply_numbers(a, b):
    """Multiplies two numbers and returns the result."""
    return a * b


# Saving the returned value into a variable
result = multiply_numbers(4, 5)
print(f"The product is: {result}")


# Here is a function that returns multiple values (as a tuple)
def get_user_stats(score, bonus):
    total_score = score + bonus
    is_passed = total_score >= 50
    return total_score, is_passed


# Unpacking the returned values
final_score, status = get_user_stats(45, 10)
print(f"Final score: {final_score}, Passed: {status}")