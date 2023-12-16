grammar Python;

// Tokens
NUMBER : [0-9]+ ;
STRING : '"' ( ~["\r\n])* '"'
        | '\'' ( ~['\r\n])* '\''
        | '"""' ( ~["])* '"""';
PASS : 'pass' ;
CONTINUE : 'continue' ;
BREAK : 'break' ;
NEWLINE : '\r'?'\n';
INDENT : '\b' ('\r'?'\n')+;
DEDENT : '\f' ('\r'?'\n')+;
WS : [ \t\r\n]+ -> skip ;
IDENTIFIER : [a-zA-Z_][a-zA-Z0-9_]* ;
COMMENT : '#' ~[\r\n]* -> skip ;

// Parser Rules

// 起始规则
program : statement* EOF ;

newLines: NEWLINE+;

statement : import_statement
          | assignment_statement
          | class_definition
          | func_definition
          | if_statements
          | loop_statements
          | comment
          | pass_statement
          | continue_statement
          | break_statement
          | expression
          | return_statement;

// import 语句
import_statement : 'import' doted_name ('as' identifier)?
                 | 'from' doted_name 'import' doted_name ('as' identifier)? ;

doted_name : identifier ( '.' identifier )* ;


// 赋值语句
assignment_statement : identifier '=' expression ;

expression : expression ( 'and' | 'or' ) expression
           | func_call
           | expression '.' class_member
           | expression ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) expression
           | expression ( '+' | '-' ) expression
           | expression ( '*' | '/' | '%' ) expression
           | expression '**' expression
           | identifier
           | NUMBER
           | STRING
           | 'True'
           | 'False'
           | 'None'
           | 'not' expression
           | '(' expression ')' ;

class_member : func_call
             | identifier ;

func_call : identifier '(' func_call_params? ')' ;

// pass, continue, break, comment
pass_statement : PASS ;
continue_statement : CONTINUE ;
break_statement : BREAK ;
comment : COMMENT ;

// 类定义
class_definition : 'class' identifier ( '(' identifier ')' )? ':' block;

// 函数定义
func_definition : 'def' func_name '(' func_params? ')' ':' block;

func_name : identifier ;
func_params : func_param ( ',' func_param )* ;
func_param : identifier | identifier '=' expression ;

// 函数调用
func_call_params : func_call_param ( ',' func_call_param )* ;
func_call_param : expression | identifier '=' expression | identifier;

// if 语句
if_statements : if_statement elif_statement* else_statement? ;

if_statement : 'if' expression ':' block;
elif_statement : 'elif' expression ':' block;
else_statement : 'else' ':' block;


// 循环语句
loop_statements : while_statement | for_statement;

while_statement : 'while' expression ':' block;
for_statement : 'for' identifier 'in' expression ':' block;

// return 语句
return_statement : 'return' expression? ;


// 代码缩进块
block : newLines indent (statement newLines?)+ dedent;

// 词法规则
indent : INDENT;
dedent : DEDENT;
identifier : IDENTIFIER;
