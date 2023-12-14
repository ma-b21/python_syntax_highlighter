@echo off

@REM grun: 可视化运行解析器

javac -cp antlr-4.13.1-complete.jar parser/*.java -d parserclasses
java -cp antlr-4.13.1-complete.jar;parserclasses org.antlr.v4.gui.TestRig Python pythonFile -tokens -gui sample.py