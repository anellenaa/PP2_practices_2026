# 10. camelCase -> snake_case
import re

def camel_to_snake(s):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()

print(camel_to_snake("helloWorldExample"))   # hello_world_example
print(camel_to_snake("MyVariableName"))      # my_variable_name