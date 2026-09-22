# Here is an example of multiple inheritance where a class inherits from two parent classes
class Walker:
    def walk(self):
        print("Walking on land...")


class Swimmer:
    def swim(self):
        print("Swimming in water...")


# Duck inherits from both Walker and Swimmer
class Duck(Walker, Swimmer):
    def quack(self):
        print("Duck is quacking!")


# Creating an object that can do both
donald = Duck()
donald.walk()
donald.swim()
donald.quack()