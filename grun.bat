@echo off

@REM grun: 可视化运行解析器

javac -cp antlr-4.13.1-complete.jar parser/*.java -d parserclasses
java -cp antlr-4.13.1-complete.jar;parserclasses -Dfile.encoding=UTF-8 org.antlr.v4.gui.TestRig Python program -tokens -gui processed_file.txt
