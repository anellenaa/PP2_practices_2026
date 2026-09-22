# Here is how to use the super() function to call methods from the parent class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"Hi, my name is {self.name} and I am {self.age} years old.")


class Student(Person):
    def __init__(self, name, age, student_id):
        # Using super() to initialize attributes from the parent class
        super().__init__(name, age)
        self.student_id = student_id

    def show_student_info(self):
        super().introduce()
        print(f"My student ID is {self.student_id}.")


# Creating an instance of Student
student = Student("Anel", 20, "S12345")
student.show_student_info()