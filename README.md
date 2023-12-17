# 编译大作业

基于 ANTLR 的 Python 代码高亮工具。

## 使用方法

在使用之前，请确保已经安装了 Python 和 ANTLR。

1. 克隆代码库到本地：

   ```bash
   git clone https://github.com/python_syntax_highlighter.git
   ```

2. 进入项目目录：

   ```bash
   cd python_syntax_highlighter
   ```

3. 修改`origin.py`文件，该文件为测试文件
4. `antlr4py.bat`生成Python解析器，在`parserpy/`目录下(直接运行`preprocess.py`即可)
5. `generate_gui.py`生成可视化语法分析树
6. `generate_tokens.py`生成`tokens`序列, 运行之前要运行`preprocess.py`进行预处理
