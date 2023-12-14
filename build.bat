@echo off

doskey antlr4 = java -cp antlr-4.13.1-complete.jar org.antlr.v4.Tool -o parser $*
doskey antlr4py = java -cp antlr-4.13.1-complete.jar org.antlr.v4.Tool -Dlanguage=Python3 -o parserpy $*
doskey antlr4vpy = java -cp antlr-4.13.1-complete.jar;. org.antlr.v4.Tool -Dlanguage=Python3 -no-listener -visitor -o parservpy $*