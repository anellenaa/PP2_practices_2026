# Here is an example of positional arguments where order matters
def describe_pet(animal_type, pet_name):
    print(f"I have a {animal_type} and its name is {pet_name}.")


# Calling with positional arguments
describe_pet("dog", "Rex")


# Here is an example of keyword arguments where order does not matter
describe_pet(pet_name="Murka", animal_type="cat")


# Here is an example of default arguments
def make_coffee(coffee_type="Espresso"):
    print(f"Preparing your coffee: {coffee_type}")


# Calling with default value
make_coffee()
# Calling with custom value
make_coffee("Cappuccino")