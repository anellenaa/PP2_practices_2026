# Here is the difference between class variables and instance variables
class Dog:
    # Class variable (shared by all instances)
    species = "Canis familiaris"

    def __init__(self, name, age):
        # Instance variables (unique to each instance)
        self.name = name
        self.age = age


# Creating instances of the class
dog1 = Dog("Rex", 3)
dog2 = Dog("Bella", 5)

print(f"{dog1.name} is {dog1.age} years old. Species: {dog1.species}")
print(f"{dog2.name} is {dog2.age} years old. Species: {dog2.species}")