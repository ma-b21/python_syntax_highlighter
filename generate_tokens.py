from parserpy.PythonLexer import PythonLexer
from parserpy.PythonParser import PythonParser
from parserpy.PythonListener import PythonListener
from antlr4 import *


def get_token_dict():
    token_file_path = "parserpy/PythonLexer.tokens"
    token_dict = {}
    with open(token_file_path, 'r') as f:
        token_names = f.readlines()
        token_names = [token_name.strip() for token_name in token_names]
        for token_name in token_names:
            token_name = token_name.split('=')
            key = int(token_name[1])
            value = token_name[0]
            if key in token_dict:
                break
            if 0 < key <= 16:
                value = 'OPERATOR'
            token_dict[key] = value
    token_dict[-1] = 'EOF'
    return token_dict


def generate_tokens():
    token_dict = get_token_dict()
    # 从文件或字符串读取输入
    # 或使用 StdinStream() 读取标准输入
    input_stream = FileStream("processed_file.txt", encoding='utf-8')

    # 创建词法分析器和Token流
    lexer = PythonLexer(input_stream)
    stream = CommonTokenStream(lexer)

    # 填充Token流
    stream.fill()

    # 遍历所有Token
    for token in stream.tokens:
        line = token.line
        column = token.column
        token_type = token.type
        token_value = token.text
        token_name = token_dict[token_type]
        token_start = token.start
        token_stop = token.stop
        token_index = token.tokenIndex
        if token_name == 'DEDENT' or token_name == 'INDENT':
            token_value = token_value.split(" ")[1]
        
        token = f"@{token_index}【pos:({line}, {column}) range: [{token_start}, {token_stop}] | {token_name}: '{token_value}'】"
        token = repr(token)[1:-1]
        print(token)
