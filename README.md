# 编译大作业

基于 ANTLR 的 Python 代码高亮工具。

## 使用方法

在使用之前，请确保已经安装了 Python 和 ANTLR。

1. 克隆代码库到本地：

   ```bash
   git clone https://github.com/your-repo.git
   ```

2. 进入项目目录：

   ```bash
   cd your-repo
   ```

3. 在命令行中使用 `build` 命令
4. `antlr4 Python.g4` + `grun` 来可视化分析`sample.py`中的 python 代码
5. `antlr4py Python.g4` 生成 listener python 解析器
6. `antlr4vpy Python.g4` 生成 visitor python 解析器
