# IMPORTANT: this file is named math.py, the same as the standard module.
# Remove the script folder from sys.path so `import math` loads the standard module.
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
sys.path = [p for p in sys.path if p not in ("", _here)]

import math

# 1. Degrees to radians
degree = float(input("Input degree: "))
print("Output radian:", round(math.radians(degree), 6))

# 2. Area of a trapezoid
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))
print("Expected Output:", (base1 + base2) / 2 * height)

# 3. Area of a regular polygon
n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))
area = n * s ** 2 / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", round(area, 2))

# 4. Area of a parallelogram
base = float(input("Length of base: "))
h = float(input("Height of parallelogram: "))
print("Expected Output:", base * h)