import math
import random
from typing import List, Tuple, Union
# 测试注释效果


class MyClass:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def print_coordinates(self):
        print(f"Coordinates: ({self.x}, {self.y})")


def my_function():
    try:
        with open("file.txt", "r") as file:
            for line in file:
                if random.randint(0, 1) == 0:
                    raise ValueError("Random error occurred")
                print(line.strip())
    except FileNotFoundError:
        print("File not found")
    except ValueError as e:
        print(f"ValueError: {e}")
    finally:
        return None


for i in range(10):
    if i % 2 == 0:
        print(f"{i} is even")
    else:
        print(f"{i} is odd")

my_object = MyClass(3, 4)
my_object.print_coordinates()
my_function()
a = my_function()
def my_lambda(x): return x**2
