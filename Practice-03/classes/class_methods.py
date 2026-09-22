# Here is an example of instance methods and the self parameter
class Rectangle:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    # Instance method to calculate area
    def calculate_area(self):
        return self.width * self.height


# Creating an object and calling its method
rect = Rectangle(5, 10)
area = rect.calculate_area()
print(f"The area of the rectangle is: {area}")