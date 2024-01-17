grammar Python;

// 本语法根据 https://docs.python.org/3/reference/grammar.html 中部分改编

// Parser rules
program : NEWLINES? statement* EOF ;

statement :( compound_stmts | simple_stmts (comment)? | comment ) NEWLINES;

simple_stmts : assignment
             | star_expression
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

assignment : single_target (AUGASSIGN | ASSIGN) (yield_expr | star_expression);

return_stmt: RETURN star_expression?;

raise_stmt : RAISE expression (FROM expression)?
           | RAISE
           ;

global_stmt: GLOBAL (NAME COMMA)* NAME;

comment : COMMENT;

del_stmt: DEL del_targets;

yield_stmt: yield_expr;

assert_stmt: ASSERT expression (COMMA expression)?;

import_stmt : import_name
            | import_from
            ;

import_name: IMPORT dotted_as_names;

import_from : FROM (DOT | ELLIPSIS)* dotted_name IMPORT import_from_targets
            | FROM (DOT | ELLIPSIS)+ IMPORT import_from_targets
            ;

import_from_targets : LBAR import_from_as_names (COMMA)? RBAR
                    | import_from_as_names
                    | '*'
                    ;

import_from_as_names: import_from_as_name (COMMA import_from_as_name)*;

import_from_as_name: NAME (AS NAME)?;

dotted_as_names: (dotted_name (AS NAME)?) (COMMA (dotted_name (AS NAME)?))*;

dotted_name : dotted_name DOT NAME
            | NAME
            ;

block : NEWLINES indent statement+ dedent 
      | simple_stmts;

indent : INDENT (NEWLINES)?;

dedent :  DEDENT (NEWLINES)?;

decorators: (AT named_expression NEWLINES)+;

class_def : (decorators)? CLASS NAME (LBAR (arguments)? RBAR)? COLON block;

function_def : (decorators)? (ASYNC)? DEF NAME LBAR (parameters)? RBAR ('->' expression)? COLON block;

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

for_stmt : FOR star_targets IN star_expression COLON block (else_block)?
         | ASYNC FOR star_targets IN star_expression COLON block (else_block)?;

with_stmt : WITH LBAR with_item (COMMA with_item)* COMMA? RBAR COLON block
          | WITH with_item (COMMA with_item)* COLON block
          | ASYNC WITH LBAR with_item (COMMA with_item)* COMMA? RBAR COLON block
          | ASYNC WITH with_item (COMMA with_item)+ COLON block;

with_item : expression AS star_target
          | expression;

try_stmt : TRY COLON block (finally_block)
         | TRY COLON block (except_block)+ (else_block)? (finally_block)?
         | TRY COLON block (except_star_block)+ (else_block)? (finally_block)?;

except_block : EXCEPT expression except_var COLON block
             | EXCEPT COLON block;

except_star_block: EXCEPT '*' expression except_var COLON block;

except_var: (AS NAME)?;

finally_block: FINALLY COLON block;

yield_expr : YIELD FROM expression
           | YIELD star_expression?
           ;

star_expression : ('*' comparison | expression) (COMMA ('*' comparison | expression))*
                 ;

star_named_expression: ('*' comparison | named_expression) (COMMA ('*' comparison | named_expression))*;

assignment_expression : NAME EXPLAIN expression ;

named_expression : assignment_expression
                 | expression
                 ;


expression : (NOT? comparison ((AND | OR) NOT? comparison)*) (IF (NOT? comparison ((AND | OR) NOT? comparison)*) ELSE expression)? (COMMA (NOT? comparison ((AND | OR) NOT? comparison)*) (IF (NOT? comparison ((AND | OR) NOT? comparison)*) ELSE expression)?)*
           | lambdef
           ;

comparison : factor ((COMPARISON_OPERATOR | (NOT IN) | IN | (IS NOT) | IS | '|' | '^' | '&' | '<<' | '>>' | '+' | '-' | '*' | '/' | '//' | '%' | AT) factor)* ;

factor : ('+' | '-' | '~') factor
       | AWAIT? atom (primary)* ('**' factor)?
       ;

primary : DOT NAME 
        | genexp 
        | LBAR arguments? RBAR 
        | LSQUARE slices RSQUARE ;

slices : slice (COMMA slice)* COMMA?;

slice : (expression)? COLON (expression)? (COLON (expression)?)?
      | named_expression;

atom : NAME
     | TRUE
     | FALSE
     | NONE
     | strings
     | NUMBER
     | (tuple | group | genexp)
     | (list | listcomp)
     | (dict | set | dictcomp | setcomp)
     | ELLIPSIS;

group: LBAR (yield_expr | named_expression) RBAR;

lambdef: LAMBDA (lambda_params)? COLON expression;

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


fstring_replacement_field : LBRACE (yield_expr | star_expression) RBRACE;

fstring_content_single : (~(LBRACE | RBRACE | '\r' | NEWLINES | '\f' | '\b' | '\''))+;

fstring_content_double : (~(LBRACE | RBRACE | '\r' | NEWLINES | '\f' | '\b' | '"'))+;

fstring : (FSTRING_START_SINGLE (fstring_content_single | fstring_replacement_field)* FSTRING_END_SINGLE)
        | (FSTRING_START_DOUBLE (fstring_content_double | fstring_replacement_field)* FSTRING_END_DOUBLE);

string: STRING;
strings: (fstring | string)+;

dict : LBRACE (double_starred_kvpairs)? RBRACE;

list: LSQUARE (star_named_expression)? RSQUARE;

tuple: LBAR (star_named_expression (COMMA star_named_expression)?)? RBAR;


set: LBRACE star_named_expression RBRACE;


double_starred_kvpairs: double_starred_kvpair (COMMA double_starred_kvpair)* (COMMA)?;

double_starred_kvpair : '**' comparison
                      | kvpair;

kvpair: expression COLON expression;

for_if_clauses: for_if_clause+;

for_if_clause : ASYNC FOR star_targets IN (((NOT? comparison) (AND (NOT? comparison))*) (OR ((NOT? comparison) (AND (NOT? comparison))*))*) (IF (((NOT? comparison) (AND (NOT? comparison))*) (OR ((NOT? comparison) (AND (NOT? comparison))*))*))*
              | FOR star_targets IN (((NOT? comparison) (AND (NOT? comparison))*) (OR ((NOT? comparison) (AND (NOT? comparison))*))*) (IF (((NOT? comparison) (AND (NOT? comparison))*) (OR ((NOT? comparison) (AND (NOT? comparison))*))*))*;

listcomp: LSQUARE named_expression for_if_clauses RSQUARE;
setcomp: LBRACE named_expression for_if_clauses RBRACE;
genexp: LBAR (assignment_expression | expression) for_if_clauses RBAR;
dictcomp: LBRACE kvpair for_if_clauses RBRACE;

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

target_with_star_atom : t_primary DOT NAME
                      | t_primary LSQUARE slices RSQUARE
                      | star_atom
                      ;

star_atom : NAME
          | LBAR target_with_star_atom RBAR
          | LBAR star_targets_tuple_seq? RBAR
          | LSQUARE star_targets_list_seq? RSQUARE
          ;

single_target : single_subscript_attribute_target
              | NAME
              | LBAR single_target RBAR
              ;

single_subscript_attribute_target : t_primary DOT NAME
                                  | t_primary LSQUARE slices RSQUARE
                                  ;

t_primary : t_primary DOT NAME
          | t_primary LSQUARE slices RSQUARE
          | t_primary genexp
          | t_primary LBAR arguments? RBAR
          | atom
          ;

del_targets: del_target (COMMA del_target)* COMMA?;

del_target : t_primary DOT NAME
           | t_primary LSQUARE slices RSQUARE
           | del_t_atom
           ;

del_t_atom : NAME
    | LBAR del_target RBAR
    | LBAR del_targets? RBAR
    | LSQUARE del_targets? RSQUARE
    ;

// Lexer rules
NEWLINES : ('\r'? '\n')+ ;
INDENT : '\b' ' ' NUMBER ;
DEDENT : '\f' ' ' NUMBER ;
FSTRING_START_SINGLE : (SF | BF) '\'';
FSTRING_START_DOUBLE : (SF | BF) '"';
SF : 'f';
BF : 'F';
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
AND : 'and' ;
OR : 'or' ;
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
         
EXPLAIN : ':=';

NAME : [a-zA-Z_] [a-zA-Z_0-9]* ;
NUMBER : [0-9]+ (DOT [0-9]*)? ;
COMMENT : '#' ~[\r\n]*;
WS: [ \t]+ -> channel(HIDDEN);
