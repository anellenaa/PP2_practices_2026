# Here is a list of numbers for filtering
numbers = [10, 15, 20, 25, 30, 35]

# Here is how to use filter() with a lambda to keep only numbers greater than 20
filtered_numbers = list(filter(lambda x: x > 20, numbers))
print(filtered_numbers)  