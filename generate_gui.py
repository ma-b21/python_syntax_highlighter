import os
from preprocess import pre_process


# 执行命令: antlr4 Python.g4
if __name__ == '__main__':
    pre_process()
    os.system('antlr4 Python.g4')
    os.system('grun')
