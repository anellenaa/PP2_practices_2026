# Here is the basic relationship between a parent (superclass) and child (subclass) class
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} is eating.")


# Dog inherits from Animal
class Dog(Animal):
    def bark(self):
        print(f"{self.name} says Woof!")


# Creating an object of the child class and using both parent and child methods
my_dog = Dog("Buddy")
my_dog.eat()  
my_dog.bark()  