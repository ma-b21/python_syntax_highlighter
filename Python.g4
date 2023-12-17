grammar Python;

// Lexer rules
// (Note: Token definitions would need to be added here based on the PEG grammar's tokens)
NEWLINE : '\r'? '\n' ;
INDENT : '\b' ('\r'? '\n')? ;
DEDENT : '\f' ('\r'? '\n')? ;
PASS : 'pass' ;
BREAK : 'break' ;
CONTINUE : 'continue' ;
NAME : [a-zA-Z_] [a-zA-Z_0-9]* ;
NUMBER : [0-9]+ ('.' [0-9]*)? ;
TYPE_COMMENT : [a-zA-Z_] [a-zA-Z_0-9]* ;
STRING : '"' ~["\r\n]* '"' | '\'' ~['\r\n]* '\'' ;
ASYNC : 'async' ;
AWAIT : 'await' ;
FSTRING_START : 'f' ;
FSTRING_MIDDLE : '{' ~[{}\r\n]* '}' ;
FSTRING_END : '}' ;
COMMENT : '#' ~[\r\n]* ;

// Parser rules
program : statements EOF ;
func_type : '(' type_expressions? ')' '->' expression NEWLINE* EOF ;

statements : statement* ;
statement :( compound_stmts | simple_stmts | comment ) NEWLINE*;

newLines : NEWLINE+ ;

simple_stmts : assignment
             | star_expressions
             | return_stmt
             | import_stmt
             | raise_stmt
             | PASS
             | del_stmt
             | yield_stmt
             | assert_stmt
             | BREAK
             | CONTINUE
             | global_stmt;

compound_stmts : function_def
               | if_stmt
               | class_def
               | for_stmt
               | try_stmt
               | with_stmt
               | while_stmt
               | match_stmt;

assignment : single_target augassign (yield_expr | star_expressions)
           | single_target '=' (yield_expr | star_expressions) NEWLINE*;


augassign : '+='
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

return_stmt: 'return' star_expressions?;

raise_stmt : 'raise' expression ('from' expression)?
           | 'raise'
           ;

global_stmt: 'global' (NAME ',')* NAME;

comment : COMMENT;

del_stmt: 'del' del_targets;

yield_stmt: yield_expr;

assert_stmt: 'assert' expression (',' expression)?;

import_stmt : import_name
            | import_from
            ;

import_name: 'import' dotted_as_names;

import_from : 'from' ('.' | '...')* dotted_name 'import' import_from_targets
            | 'from' ('.' | '...')+ 'import' import_from_targets
            ;

import_from_targets : '(' import_from_as_names (',')? ')'
                    | import_from_as_names
                    | '*'
                    ;

import_from_as_names: import_from_as_name (',' import_from_as_name)*;

import_from_as_name: NAME ('as' NAME)?;

dotted_as_names: dotted_as_name (',' dotted_as_name)*;

dotted_as_name: dotted_name ('as' NAME)?;

dotted_name : dotted_name '.' NAME
            | NAME
            ;

// ANTLR grammar conversion from PEG (Continued)

block : NEWLINE INDENT statements DEDENT 
      | simple_stmts;

decorators: ('@' named_expression NEWLINE)+;

class_def : (decorators)? class_def_raw;

class_def_raw : 'class' NAME (type_params)? ('(' (arguments)? ')')? ':' block;

function_def : (decorators)? function_def_raw;

function_def_raw : 'def' NAME (type_params)? '(' (params)? ')' ('->' expression)? ':' (func_type_comment)? block
                 | ASYNC 'def' NAME (type_params)? '(' (params)? ')' ('->' expression)? ':' (func_type_comment)? block;

params : (parameters)?;

parameters : slash_no_default (param_no_default)* (param_with_default)* (star_etc)?
           | slash_with_default (param_with_default)* (star_etc)?
           | (param_no_default)+ (param_with_default)* (star_etc)?
           | (param_with_default)+ (star_etc)?
           | star_etc;

slash_no_default : (param_no_default)+ '/'
                 | (param_no_default)+ '/'?;

slash_with_default : (param_no_default)* (param_with_default)+ '/'
                   | (param_no_default)* (param_with_default)+ '/'?;

star_etc : '*' param_no_default (param_maybe_default)* (kwds)?
         | '*' ',' (param_maybe_default)+ (kwds)?
         | kwds;

kwds : '**' param_no_default;

param_no_default : param ','
                 | param;

param_with_default : param default ','
                   | param default;

param_maybe_default : param (default)? ','
                    | param (default)?;

param : NAME (annotation)?;

annotation : ':' expression;

default : '=' expression;

if_stmt : 'if' named_expression ':' block (elif_stmt)?
        | 'if' named_expression ':' block (else_block)?;

elif_stmt : 'elif' named_expression ':' block (elif_stmt)?
          | 'elif' named_expression ':' block (else_block)?;

else_block: 'else' ':' block;

while_stmt: 'while' named_expression ':' block (else_block)?;

for_stmt : 'for' star_targets 'in' star_expressions ':' (TYPE_COMMENT)? block (else_block)?
         | ASYNC 'for' star_targets 'in' star_expressions ':' (TYPE_COMMENT)? block (else_block)?;

with_stmt : 'with' '(' with_item (',' with_item)* ','? ')' ':' block
          | 'with' with_item (',' with_item)* ':' (TYPE_COMMENT)? block
          | ASYNC 'with' '(' with_item (',' with_item)* ','? ')' ':' block
          | ASYNC 'with' with_item (',' with_item)+ ':' (TYPE_COMMENT)? block;

with_item : expression 'as' star_target
          | expression;

try_stmt : 'try' ':' block (finally_block)
         | 'try' ':' block (except_block)+ (else_block)? (finally_block)?
         | 'try' ':' block (except_star_block)+ (else_block)? (finally_block)?;

except_block : 'except' expression ('as' NAME)? ':' block
             | 'except' ':' block;

except_star_block: 'except' '*' expression ('as' NAME)? ':' block;

finally_block: 'finally' ':' block;

// ANTLR grammar conversion from PEG (Continued)

match_stmt : 'match' subject_expr ':' NEWLINE INDENT case_block+ DEDENT;

subject_expr : star_named_expression ',' star_named_expressions?
             | named_expression;

case_block : 'case' patterns guard? ':' block;

guard: 'if' named_expression;

patterns : open_sequence_pattern
    | pattern;

pattern : as_pattern
    | or_pattern;

as_pattern : or_pattern 'as' pattern_capture_target;

or_pattern : closed_pattern ('|' closed_pattern)+;

closed_pattern : literal_pattern
               | capture_pattern
               | wildcard_pattern
               | value_pattern
               | group_pattern
               | sequence_pattern
               | mapping_pattern
               | class_pattern;

literal_pattern : signed_number
                | complex_number
                | strings
                | 'None'
                | 'True'
                | 'False';

complex_number : signed_real_number '+' imaginary_number
               | signed_real_number '-' imaginary_number;

signed_number : NUMBER
              | '-' NUMBER;

signed_real_number : real_number
                   | '-' real_number;

real_number: NUMBER;
imaginary_number: NUMBER;

capture_pattern : pattern_capture_target;

pattern_capture_target : NAME;

wildcard_pattern: '_';

value_pattern : attr;

attr : name_or_attr '.' NAME;

name_or_attr : NAME;

group_pattern : '(' pattern ')';

sequence_pattern : '[' maybe_sequence_pattern? ']'
                 | '(' open_sequence_pattern? ')';

open_sequence_pattern : maybe_star_pattern ',' maybe_sequence_pattern?;

maybe_sequence_pattern : maybe_star_pattern (',' maybe_star_pattern)*;

maybe_star_pattern : star_pattern
                   | pattern;

star_pattern : '*' pattern_capture_target
             | '*' wildcard_pattern;

mapping_pattern : '{' '}'
                | '{' double_star_pattern ','? '}'
                | '{' items_pattern ',' double_star_pattern ','? '}'
                | '{' items_pattern ','? '}';

items_pattern : key_value_pattern (',' key_value_pattern)*;

key_value_pattern : (literal_expr | attr) ':' pattern;

literal_expr : literal_pattern
             | NAME;

double_star_pattern : '**' pattern_capture_target;

class_pattern : name_or_attr '(' ')'
              | name_or_attr '(' positional_patterns ','? ')'
              | name_or_attr '(' keyword_patterns ','? ')'
              | name_or_attr '(' positional_patterns ',' keyword_patterns ','? ')';

// ANTLR grammar conversion from PEG (Continued)

positional_patterns: pattern (',' pattern)*;

keyword_patterns: keyword_pattern (',' keyword_pattern)*;

keyword_pattern: NAME '=' pattern;

type_params: '[' type_param_seq ']';

type_param_seq: type_param (',' type_param)*;

type_param : NAME ':' expression
           | NAME
           | '*' NAME ':' expression
           | '*' NAME
           | '**' NAME ':' expression
           | '**' NAME
           ;

expressions : expression (',' expression)*
            | expression ','
            | expression
            ;

expression : disjunction 'if' disjunction 'else' expression
           | disjunction
           | lambdef
           ;

yield_expr : 'yield' 'from' expression
           | 'yield' star_expressions?
           ;

star_expressions : star_expression (',' star_expression)*
                 | star_expression ','
                 | star_expression
                 ;

star_expression : '*' bitwise_or
                | expression
                ;

star_named_expressions: star_named_expression (',' star_named_expression)*;

star_named_expression : '*' bitwise_or
                      | named_expression
                      ;

assignment_expression : NAME ':=' expression ;

named_expression : assignment_expression
                 | expression
              ;

disjunction : conjunction ('or' conjunction)*
            | conjunction
            ;

conjunction : inversion ('and' inversion)*
            | inversion
            ;

inversion : 'not' inversion
          | comparison
          ;

comparison : bitwise_or compare_op_bitwise_or_pair*
           | bitwise_or
           ;

compare_op_bitwise_or_pair : comparison_operator bitwise_or ;

comparison_operator : '=='
                    | '!='
                    | '<='
                    | '<'
                    | '>='
                    | '>'
                    | 'not' 'in'
                    | 'in'
                    | 'is' 'not'
                    | 'is'
                    ;

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

// ANTLR grammar conversion from PEG (Continued)

slices : slice (',' slice)* ','?
       | slice;

slice : (expression)? ':' (expression)? (':' (expression)?)?
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

lambdef: 'lambda' (lambda_params)? ':' expression;

lambda_params: lambda_parameters;

lambda_parameters : lambda_slash_no_default (lambda_param_no_default)* (lambda_param_with_default)* (lambda_star_etc)?
                  | lambda_slash_with_default (lambda_param_with_default)* (lambda_star_etc)?
                  | (lambda_param_no_default)+ (lambda_param_with_default)* (lambda_star_etc)?
                  | (lambda_param_with_default)+ (lambda_star_etc)?
                  | lambda_star_etc;

lambda_slash_no_default : (lambda_param_no_default)+ '/' ','
                        | (lambda_param_no_default)+ '/'?;

lambda_slash_with_default : (lambda_param_no_default)* (lambda_param_with_default)+ '/' ','
                          | (lambda_param_no_default)* (lambda_param_with_default)+ '/'?;

lambda_star_etc : '*' lambda_param_no_default (lambda_param_maybe_default)* (lambda_kwds)?
                | '*' ',' (lambda_param_maybe_default)+ (lambda_kwds)?
                | lambda_kwds;

lambda_kwds: '**' lambda_param_no_default;

lambda_param_no_default : lambda_param ','
                        | lambda_param;

lambda_param_with_default : lambda_param default ','
                          | lambda_param default;

lambda_param_maybe_default  : lambda_param (default)? ','
                            | lambda_param (default)?;

lambda_param: NAME;

// ANTLR grammar conversion from PEG (Continued)

fstring_middle : fstring_replacement_field
               | FSTRING_MIDDLE;

fstring_replacement_field : '{' (yield_expr | star_expressions) (fstring_conversion)? (fstring_full_format_spec)? '}';

fstring_conversion : '!' NAME;

fstring_full_format_spec : ':' fstring_format_spec*;

fstring_format_spec : FSTRING_MIDDLE
                    | fstring_replacement_field;

fstring : FSTRING_START fstring_middle* FSTRING_END;

string: STRING;
strings: (fstring | string)+;

list: '[' (star_named_expressions)? ']';

tuple: '(' (star_named_expression (',' star_named_expressions)?)? ')';

set: '{' star_named_expressions '}';

dict : '{' (double_starred_kvpairs)? '}';

double_starred_kvpairs: double_starred_kvpair (',' double_starred_kvpair)* (',')?;

double_starred_kvpair : '**' bitwise_or
                      | kvpair;

kvpair: expression ':' expression;

for_if_clauses: for_if_clause+;

for_if_clause : ASYNC 'for' star_targets 'in' disjunction ('if' disjunction)*
              | 'for' star_targets 'in' disjunction ('if' disjunction)*;

listcomp: '[' named_expression for_if_clauses ']';
setcomp: '{' named_expression for_if_clauses '}';
genexp: '(' (assignment_expression | expression) for_if_clauses ')';
dictcomp: '{' kvpair for_if_clauses '}';

arguments :  (args (',' args)* (',' kwargs)? | kwargs) (',')?;

args : (starred_expression | (assignment_expression | expression));

kwargs : kwarg_or_starred (',' kwarg_or_double_starred)*
       | kwarg_or_starred+
       | kwarg_or_double_starred+;

starred_expression: '*' expression;

kwarg_or_starred : NAME '=' expression
                 | starred_expression;

kwarg_or_double_starred : NAME '=' expression
                        | '**' expression;

// ANTLR grammar conversion from PEG (Continued)

star_targets : star_target
             | star_target (',' star_target)* ','?
             ;

star_targets_list_seq: star_target (',' star_target)* ','?;

star_targets_tuple_seq : star_target (',' star_target)+ ','?
                       | star_target ','
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

t_lookahead: '(' | '[' | '.';

del_targets: del_target (',' del_target)* ','?;

del_target : t_primary '.' NAME
           | t_primary '[' slices ']'
           | del_t_atom
           ;

del_t_atom : NAME
    | '(' del_target ')'
    | '(' del_targets? ')'
    | '[' del_targets? ']'
    ;

type_expressions : expression (',' expression)* ',' '*' expression ',' '**' expression
                 | expression (',' expression)* ',' '*' expression
                 | expression (',' expression)* ',' '**' expression
                 | '*' expression ',' '**' expression
                 | '*' expression
                 | '**' expression
                 | expression (',' expression)*
                 ;

func_type_comment : NEWLINE TYPE_COMMENT
                  | TYPE_COMMENT
                  ;
