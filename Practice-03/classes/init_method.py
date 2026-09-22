# Here is how to use the __init__ constructor method to initialize object attributes
class Car:

    def __init__(self, brand, year):
        self.brand = brand
        self.year = year


# Creating objects with different initial values
car1 = Car("Toyota", 2022)
car2 = Car("Tesla", 2025)

print(f"Car 1: {car1.brand}, Year: {car1.year}")
print(f"Car 2: {car2.brand}, Year: {car2.year}")