grammar Python;

// Tokens
NUMBER : [0-9]+ ;
STRING : '"' ~["]* '"' ;
PASS : 'pass' ;
CONTINUE : 'continue' ;
BREAK : 'break' ;
NEWLINE : '\r'?'\n';
INDENT : '\b' ;
DEDENT : '\f' ;
WS : [ \t]+ -> skip ;
IDENTIFIER : [a-zA-Z_][a-zA-Z0-9_]* ;
COMMENT : '#' ~[\r\n]* ;

// Parser Rules

program : (statement newLines)* statement newLines? EOF ;

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
          | break_statement;

import_statement : 'import' identifier ( '.' identifier )* ('as' identifier)?
                 | 'from' identifier 'import' identifier ( '.' identifier ( '.' identifier )*)? ('as' identifier)? ;

assignment_statement : identifier '=' expression ;

expression : expression ( 'and' | 'or' ) expression
           | expression ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) expression
           | expression ( '+' | '-' ) expression
           | expression ( '*' | '/' | '%' ) expression
           | expression '**' expression
           | expression '.' identifier
           | identifier
           | NUMBER
           | STRING
           | 'True'
           | 'False'
           | 'None'
           | 'not' expression
           | '(' expression ')' ;

pass_statement : PASS ;
continue_statement : CONTINUE ;
break_statement : BREAK ;
comment : COMMENT ;


class_definition : 'class' identifier ( '(' identifier ')' )? ':' block;

func_definition : 'def' func_name '(' func_params? ')' ':' block;

func_name : identifier ;
func_params : identifier ( ',' identifier )*
            | identifier '=' expression ( ',' identifier '=' expression )* ;

if_statements : if_statement elif_statement* else_statement? ;

if_statement : 'if' expression ':' block;
elif_statement : 'elif' expression ':' block;
else_statement : 'else' ':' block;

loop_statements : while_statement | for_statement;

while_statement : 'while' expression ':' block;

for_statement : 'for' identifier 'in' expression ':' block;

block : newLines indent (statement newLines?)+ dedent;

indent : INDENT newLines;
dedent : DEDENT newLines;
identifier : IDENTIFIER ;

