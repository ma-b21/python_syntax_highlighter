import tokenize
import ast
import io

# # 1. 引入其他包的语句
# import math

# # 2. 类的定义及对应变量的初始化
# class MyClass:
#     def __init__(self, x):
#         self.x = x

#     def print_x(self):
#         print(self.x)

# # 3. 函数定义及其调用
# def my_function():
#     print("Hello, World!")

# my_function()

# # 4. 类变量对应的成员函数的调用
# obj = MyClass(42)
# obj.print_x()

# # 5. 字符串常量与数值型常量
# string_constant = "Hello, String!"
# number_constant = 123

# # 6. 算术运算符和逻辑运算符
# result = 10 + 5 * 2
# logical_result = True and False

# # 7. 条件判断语句与循环语句
# if result > 15:
#     print("Result is greater than 15")
# else:
#     print("Result is not greater than 15")

# for i in range(3):
#     print(i)

# 词法分析
code = """
import math
class MyClass:
    def __init__(self, x):
        self.x = x

    def print_x(self):
        print(self.x)

def my_function():
    print("Hello, World!")

my_function()

obj = MyClass(42)
obj.print_x()

string_constant = "Hello, String!"
number_constant = 123

result = 10 + 5 * 2
logical_result = True and False

if result > 15:
    print("Result is greater than 15")
else:
    print("Result is not greater than 15")

for i in range(3):
    print(i)
"""

tokens = tokenize.tokenize(io.BytesIO(code.encode("utf-8")).readline)

for token in tokens:
    print(token)

# 语法分析
tree = ast.parse(code)
ast.dump(tree)
