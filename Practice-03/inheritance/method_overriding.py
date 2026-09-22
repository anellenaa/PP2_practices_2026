# Here is an example of method overriding where a child class modifies parent's method
class Bird:
    def make_sound(self):
        print("Some generic bird sound")


class Duck(Bird):
    # Overriding the parent's method
    def make_sound(self):
        print("Quack! Quack!")


# Testing method overriding
generic_bird = Bird()
generic_bird.make_sound()

my_duck = Duck()
my_duck.make_sound() 