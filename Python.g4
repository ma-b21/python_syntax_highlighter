grammar Python;

// 本语法根据 https://docs.python.org/3/reference/grammar.html 中部分改编

// Parser rules
program : statement* EOF ;

statement :( compound_stmts | simple_stmts (comment)? | comment ) NEWLINES;

simple_stmts : assignment
             | star_expressions
             | return_stmt
             | import_stmt
             | raise_stmt
             | pass_stmt
             | del_stmt
             | yield_stmt
             | assert_stmt
             | break_stmt
             | continue_stmt
             | global_stmt;

pass_stmt : PASS;
break_stmt : BREAK;
continue_stmt : CONTINUE;

compound_stmts : function_def
               | if_stmt
               | class_def
               | for_stmt
               | try_stmt
               | with_stmt
               | while_stmt;

assignment : single_target augassign (yield_expr | star_expressions);

augassign : AUGASSIGN | ASSIGN;

return_stmt: RETURN star_expressions?;

raise_stmt : RAISE expression (FROM expression)?
           | RAISE
           ;

global_stmt: GLOBAL (NAME COMMA)* NAME;

comment : COMMENT;

del_stmt: 'del' del_targets;

yield_stmt: yield_expr;

assert_stmt: 'assert' expression (COMMA expression)?;

import_stmt : import_name
            | import_from
            ;

import_name: IMPORT dotted_as_names;

import_from : FROM ('.' | '...')* dotted_name IMPORT import_from_targets
            | FROM ('.' | '...')+ IMPORT import_from_targets
            ;

import_from_targets : '(' import_from_as_names (COMMA)? ')'
                    | import_from_as_names
                    | '*'
                    ;

import_from_as_names: import_from_as_name (COMMA import_from_as_name)*;

import_from_as_name: NAME (AS NAME)?;

dotted_as_names: dotted_as_name (COMMA dotted_as_name)*;

dotted_as_name: dotted_name (AS NAME)?;

dotted_name : dotted_name '.' NAME
            | NAME
            ;

block : NEWLINES indent statement+ dedent 
      | simple_stmts;

indent : INDENT (NEWLINES)?;

dedent : DEDENT (NEWLINES)?;

decorators: ('@' named_expression NEWLINES)+;

class_def : (decorators)? CLASS NAME ('(' (arguments)? ')')? COLON block;

function_def : (decorators)? (ASYNC)? DEF NAME '(' (parameters)? ')' ('->' expression)? COLON block;

parameters : (param_no_default)+ (param_with_default)* (star_etc)?
           | (param_with_default)+ (star_etc)?
           | star_etc;

star_etc : '*' param_no_default (param_maybe_default)* (kwds)?
         | '*' COMMA (param_maybe_default)+ (kwds)?
         | kwds;

kwds : '**' param_no_default;

param_no_default : param COMMA
                 | param;

param_with_default : param default COMMA
                   | param default;

param_maybe_default : param (default)? COMMA
                    | param (default)?;

param : NAME (annotation)?;

annotation : COLON expression;

default : ASSIGN expression;

if_stmt : IF named_expression COLON block (elif_stmt)?
        | IF named_expression COLON block (else_block)?;

elif_stmt : ELIF named_expression COLON block (elif_stmt)?
          | ELIF named_expression COLON block (else_block)?;

else_block: ELSE COLON block;

while_stmt: WHILE named_expression COLON block (else_block)?;

for_stmt : FOR star_targets IN star_expressions COLON block (else_block)?
         | ASYNC FOR star_targets IN star_expressions COLON block (else_block)?;

with_stmt : WITH '(' with_item (COMMA with_item)* COMMA? ')' COLON block
          | WITH with_item (COMMA with_item)* COLON block
          | ASYNC WITH '(' with_item (COMMA with_item)* COMMA? ')' COLON block
          | ASYNC WITH with_item (COMMA with_item)+ COLON block;

with_item : expression AS star_target
          | expression;

try_stmt : 'try' COLON block (finally_block)
         | 'try' COLON block (except_block)+ (else_block)? (finally_block)?
         | 'try' COLON block (except_star_block)+ (else_block)? (finally_block)?;

except_block : EXCEPT expression (AS NAME)? COLON block
             | EXCEPT COLON block;

except_star_block: EXCEPT '*' expression (AS NAME)? COLON block;

finally_block: FINALLY COLON block;

yield_expr : 'yield' FROM expression
           | 'yield' star_expressions?
           ;

star_expressions : star_expression (COMMA star_expression)*
                 | star_expression COMMA
                 | star_expression
                 ;

star_expression : '*' bitwise_or
                | expression
                ;

star_named_expressions: star_named_expression (COMMA star_named_expression)*;

star_named_expression : '*' bitwise_or
                      | named_expression
                      ;

assignment_expression : NAME EXPLAIN expression ;

named_expression : assignment_expression
                 | expression
              ;


expressions : expression (COMMA expression)*
            | expression COMMA
            | expression
            ;

expression : disjunction IF disjunction ELSE expression
           | atom
           | primary
           | await_primary
           | power
           | factor
           | term
           | sum
           | shift_expr
           | bitwise_and
           | bitwise_xor
           | bitwise_or
           | comparison
           | inversion
           | conjunction
           | disjunction
           | lambdef
           ;

disjunction : conjunction ('or' conjunction)* ;

conjunction : inversion ('and' inversion)* ;

inversion : NOT inversion | comparison ;

comparison : bitwise_or compare_op_bitwise_or_pair* ;

compare_op_bitwise_or_pair : COMPARISON_OPERATOR bitwise_or ;

bitwise_or : bitwise_or '|' bitwise_xor
           | bitwise_xor
           ;

bitwise_xor : bitwise_xor '^' bitwise_and
            | bitwise_and
            ;

bitwise_and : bitwise_and '&' shift_expr
            | shift_expr
            ;

shift_expr : shift_expr ('<<' | '>>') sum
           | sum
           ;

sum : sum ('+' | '-') term
    | term
    ;

term : term ('*' | '/' | '//' | '%' | '@') factor
     | factor
     ;

factor : ('+' | '-' | '~') factor
       | power
       ;

power : await_primary '**' factor
      | await_primary
      ;

await_primary : AWAIT primary
              | primary
              ;

primary : primary '.' NAME
        | primary genexp
        | primary '(' arguments? ')'
        | primary '[' slices ']'
        | atom
        ;

slices : slice (COMMA slice)* COMMA?
       | slice;

slice : (expression)? COLON (expression)? (COLON (expression)?)?
      | named_expression;

atom : NAME
     | 'True'
     | 'False'
     | 'None'
     | strings
     | NUMBER
     | (tuple | group | genexp)
     | (list | listcomp)
     | (dict | set | dictcomp | setcomp)
     | '...';

group: '(' (yield_expr | named_expression) ')';

lambdef: 'lambda' (lambda_params)? COLON expression;

lambda_params: lambda_parameters;

lambda_parameters : (lambda_param_no_default)+ (lambda_param_with_default)* (lambda_star_etc)?
                  | (lambda_param_with_default)+ (lambda_star_etc)?
                  | lambda_star_etc;

lambda_star_etc : '*' lambda_param_no_default (lambda_param_maybe_default)* (lambda_kwds)?
                | '*' COMMA (lambda_param_maybe_default)+ (lambda_kwds)?
                | lambda_kwds;

lambda_kwds: '**' lambda_param_no_default;

lambda_param_no_default : lambda_param COMMA
                        | lambda_param;

lambda_param_with_default : lambda_param default COMMA
                          | lambda_param default;

lambda_param_maybe_default  : lambda_param (default)? COMMA
                            | lambda_param (default)?;

lambda_param: NAME;


fstring_replacement_field : '{' (yield_expr | star_expressions) '}';

fstring_content_single : (~('{' | '}' | '\r' | '\n' | '\f' | '\b' | '\''))+;

fstring_content_double : (~('{' | '}' | '\r' | '\n' | '\f' | '\b' | '"'))+;

fstring : (FSTRING_START_SINGLE (fstring_content_single | fstring_replacement_field)* FSTRING_END_SINGLE)
        | (FSTRING_START_DOUBLE (fstring_content_double | fstring_replacement_field)* FSTRING_END_DOUBLE);

string: STRING;
strings: (fstring | string)+;

dict : '{' (double_starred_kvpairs)? '}';

list: '[' (star_named_expressions)? ']';

tuple: '(' (star_named_expression (COMMA star_named_expressions)?)? ')';


set: '{' star_named_expressions '}';


double_starred_kvpairs: double_starred_kvpair (COMMA double_starred_kvpair)* (COMMA)?;

double_starred_kvpair : '**' bitwise_or
                      | kvpair;

kvpair: expression COLON expression;

for_if_clauses: for_if_clause+;

for_if_clause : ASYNC FOR star_targets IN disjunction (IF disjunction)*
              | FOR star_targets IN disjunction (IF disjunction)*;

listcomp: '[' named_expression for_if_clauses ']';
setcomp: '{' named_expression for_if_clauses '}';
genexp: '(' (assignment_expression | expression) for_if_clauses ')';
dictcomp: '{' kvpair for_if_clauses '}';

arguments :  (args (COMMA args)* (COMMA kwargs)? | kwargs) (COMMA)?;

args : (starred_expression | (assignment_expression | expression));

kwargs : kwarg_or_starred (COMMA kwarg_or_double_starred)*
       | kwarg_or_starred+
       | kwarg_or_double_starred+;

starred_expression: '*' expression;

kwarg_or_starred : NAME ASSIGN expression
                 | starred_expression;

kwarg_or_double_starred : NAME ASSIGN expression
                        | '**' expression;

star_targets : star_target
             | star_target (COMMA star_target)* COMMA?
             ;

star_targets_list_seq: star_target (COMMA star_target)* COMMA?;

star_targets_tuple_seq : star_target (COMMA star_target)+ COMMA?
                       | star_target COMMA
                       ;

star_target : '*' (star_target)
            | target_with_star_atom
            ;

target_with_star_atom : t_primary '.' NAME
                      | t_primary '[' slices ']'
                      | star_atom
                      ;

star_atom : NAME
          | '(' target_with_star_atom ')'
          | '(' star_targets_tuple_seq? ')'
          | '[' star_targets_list_seq? ']'
          ;

single_target : single_subscript_attribute_target
              | NAME
              | '(' single_target ')'
              ;

single_subscript_attribute_target : t_primary '.' NAME
                                  | t_primary '[' slices ']'
                                  ;

t_primary : t_primary '.' NAME
          | t_primary '[' slices ']'
          | t_primary genexp
          | t_primary '(' arguments? ')'
          | atom
          ;

del_targets: del_target (COMMA del_target)* COMMA?;

del_target : t_primary '.' NAME
           | t_primary '[' slices ']'
           | del_t_atom
           ;

del_t_atom : NAME
    | '(' del_target ')'
    | '(' del_targets? ')'
    | '[' del_targets? ']'
    ;

// Lexer rules
ENTER : '\r' ;
LINEBREAK : '\n' ;
NEWLINES : (ENTER? LINEBREAK)+ ;
INDENT : '\b' ' ' NUMBER ;
DEDENT : '\f' ' ' NUMBER ;
FSTRING_START_SINGLE : 'f\'' | 'F\'';
FSTRING_START_DOUBLE : 'f"' | 'F"';
FSTRING_END_SINGLE : '\'';
FSTRING_END_DOUBLE : '"';
STRING : '"' ~["\r\n]* '"' | '\'' ~['\r\n]* '\'' ;
AUGASSIGN : '+='
          | '-='
          | '*='
          | '@='
          | '/='
          | '%='
          | '&='
          | '|='
          | '^='
          | '<<='
          | '>>='
          | '**='
          | '//=';
ASSIGN : '=';

IF : 'if' ;
ELSE : 'else' ;
ELIF : 'elif' ;
FOR : 'for' ;
IN : 'in' ;
NOT : 'not' ;
IS : 'is' ;
WHILE : 'while' ;
DEF : 'def' ;
RETURN : 'return' ;
CLASS : 'class' ;
WITH : 'with' ;
AS : 'as' ;
EXCEPT : 'except' ;
FINALLY : 'finally' ;
FROM : 'from' ;
IMPORT : 'import' ;
PASS : 'pass' ;
BREAK : 'break' ;
CONTINUE : 'continue' ;
GLOBAL : 'global' ;
RAISE : 'raise' ;
DEL : 'del' ;
ASSERT : 'assert' ;
ASYNC : 'async' ;
AWAIT : 'await' ;
TRY : 'try' ;
YIELD : 'yield' ;
TRUE : 'True' ;
FALSE : 'False' ;
NONE : 'None' ;
LAMBDA : 'lambda' ;

COMPARISON_OPERATOR : '=='
                    | '!='
                    | '<='
                    | '<'
                    | '>='
                    | '>'
                    | NOT IN
                    | IN
                    | IS NOT
                    | IS
                    ;
COMMA : ',' ;
COLON : ':' ;
DOT : '.' ;
ELLIPSIS : '...' ;
AT : '@' ;
LBAR : '(' ;
RBAR : ')' ;
LSQUARE : '[' ;
RSQUARE : ']' ;
LBRACE : '{' ;
RBRACE : '}' ;
OPERATOR : '*'
         | '->'
         | '**'
         | 'or'
         | 'and'
         | '|'
         | '^'
         | '&'
         | '<<'
         | '>>'
         | '+'
         | '-'
         | '/'
         | '//'
         | '%'
         | '~'
         ;
         
EXPLAIN : ':=';

NAME : [a-zA-Z_] [a-zA-Z_0-9]* ;
NUMBER : [0-9]+ ('.' [0-9]*)? ;
COMMENT : '#' ~[\r\n]*;
WS: [ \t]+ -> skip ;