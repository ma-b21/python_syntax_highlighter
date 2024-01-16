from antlr4 import *
from parserpy.PythonLexer import PythonLexer
from parserpy.PythonParser import PythonParser
import json

def tree_to_json(tree, rule_names):
    """
    Recursively walk the ANTLR4 parse tree and convert it to a JSON object.
    """
    if tree is None:
        return None

    # Terminal node
    if isinstance(tree, TerminalNode):
        return {
            'type': 'Terminal',
            'text': tree.getText()
        }

    # Parser rule
    json_obj = {
        'type': 'Rule',
        'rule': rule_names[tree.getRuleIndex()],
        'children': []
    }

    # Recursively add children
    for i in range(tree.getChildCount()):
        child = tree.getChild(i)
        json_obj['children'].append(tree_to_json(child, rule_names))

    return json_obj

def main():
    # Read input file
    input_code = FileStream("processed_file.txt", encoding='utf-8')

    # Initialize lexer and parser
    lexer = PythonLexer(input_code)
    stream = CommonTokenStream(lexer)
    parser = PythonParser(stream)

    # Parse the input and convert the parse tree to JSON
    parse_tree = parser.program()
    json_tree = tree_to_json(parse_tree, PythonParser.ruleNames)

    # Save the JSON tree to a file
    with open('parse_tree.json', 'w', encoding='utf-8') as json_file:
        json.dump(json_tree, json_file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()