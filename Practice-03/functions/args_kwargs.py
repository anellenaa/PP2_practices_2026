# Here is an example of using *args for arbitrary positional arguments
def sum_all_numbers(*args):
    """Sums up all given numbers."""
    total = sum(args)
    print(f"Received arguments: {args}")
    print(f"Total sum: {total}")


# Calling with different number of arguments
sum_all_numbers(1, 2, 3)
sum_all_numbers(10, 20, 30, 40, 50)


# Here is an example of using **kwargs for arbitrary keyword arguments
def print_student_profile(**kwargs):
    """Prints key-value pairs of student information."""
    print("Student Profile Details:")
    for key, value in kwargs.items():
        print(f"- {key}: {value}")


# Calling with keyword arguments
print_student_profile(name="Anel", major="Computer Science", year=2)