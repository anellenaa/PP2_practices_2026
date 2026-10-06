# 7. snake_case -> camelCase
import re

def snake_to_camel(s):
    return re.sub(r"_([a-z0-9])", lambda m: m.group(1).upper(), s)

print(snake_to_camel("hello_world_example"))   # helloWorldExample
print(snake_to_camel("my_variable_name"))      # myVariableName