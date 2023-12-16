import os
def preprocess_python_code(file_path):
    INDENT_CHAR = '\b'
    DEDENT_CHAR = '\f'

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    stack = [0]  # 缩进栈，栈顶元素是当前缩进级别

    for line in lines:
        stripped_line = line.lstrip()
        indent_level = len(line) - len(stripped_line)

        if stripped_line:  # 非空行
            while stack and stack[-1] > indent_level:
                stack.pop()
                new_lines.append(DEDENT_CHAR + '\n')  # 缩进退格后增加一行DEDENT

            if not stack or indent_level > stack[-1]:
                stack.append(indent_level)
                new_lines.append(INDENT_CHAR + '\n')  # 增加缩进级别时在上方增加一行INDENT
                new_lines.append(line)
            else:
                new_lines.append(line)
        else:  # 空行或注释行
            new_lines.append(line)
    new_lines.append('\n')  # 文件结束时增加一个空行
    while stack and stack[-1] > 0:
        stack.pop()
        new_lines.append(DEDENT_CHAR + '\n')  # 文件结束时增加DEDENT行

    return ''.join(new_lines)

# 使用示例
file_path = 'origin.py'
processed_code = preprocess_python_code(file_path)

with open('processed_file.txt', 'w') as file:
    file.write(processed_code)

# 执行命令: antlr4 Python.g4
os.system('antlr4 Python.g4')
os.system('grun')