from PythonEditor import Ui_PythonEditor
from PyQt5 import QtWidgets
from qfluentwidgets import FluentIcon, Action, TextEdit
from PyQt5 import QtCore
import os
from visitor import Visitor
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QStringListModel


class PythonEditor(QtWidgets.QMainWindow, Ui_PythonEditor):
    visitor = None
    cursurPos = None
    vvalue = None
    hvalue = None
    maxvalue = None
    time_unchanged = 0
    string_list = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.CommandBar.setIconSize(QtCore.QSize(22, 22))

        self.CommandBar.addAction(Action(FluentIcon.DOCUMENT, "Open"))
        self.CommandBar.addAction(Action(FluentIcon.SAVE_AS, "Save"))
        self.CommandBar.addAction(Action(FluentIcon.PLAY, "Run"))

        self.visitor = Visitor()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.highlight)

        # 文本改变时触发，time_unchanged置0, 开始计时
        self.Editor.textChanged.connect(self.textChanged)

        self.string_list = QStringListModel()
        self.ShowVar.setModel(self.string_list)

        # self.Editor.textChanged.connect(self.highlight)

    def readWordBeforeCursor(self):
        cursor = self.Editor.textCursor()
        word = ""

        # 检查光标是否已经在文档开始处
        if cursor.atStart():
            return word, False

        while True:
            # 向左移动光标并选中一个字符
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor)

            # 读取选中的字符
            char = cursor.selectedText()

            # 如果遇到空白字符或者文档开始，则停止
            if char.isspace() or char == "\n" or char == "\r" or char == "\t":
                return (word, False)

            if char == ".":
                return (word, True)

            # 将字符添加到单词的开头
            word = char + word

            if cursor.atStart():
                break

            # 将光标向左移动一个字符位置，不选中字符
            cursor.movePosition(QTextCursor.Left)

        return (word, False)

    def textChanged(self):
        self.time_unchanged = 0
        self.timer.start(100)

    def saveWindow(self):
        textCursor = self.Editor.textCursor()
        self.cursurPos = textCursor.position()
        # print(self.cursurPos)
        self.vvalue = self.Editor.verticalScrollBar().value()
        self.hvalue = self.Editor.horizontalScrollBar().value()
        self.maxvalue = self.Editor.verticalScrollBar().maximum()

    def restoreWindow(self):
        textCursor = self.Editor.textCursor()
        textCursor.setPosition(self.cursurPos)
        self.Editor.setTextCursor(textCursor)
        self.Editor.verticalScrollBar().setMaximum(self.maxvalue)
        self.Editor.verticalScrollBar().setValue(self.vvalue)
        self.Editor.horizontalScrollBar().setValue(self.hvalue)

    def highlight(self):
        if self.time_unchanged < 0.5:
            self.time_unchanged += 0.1
            return
        self.saveWindow()
        code = self.Editor.toPlainText()
        try:
            flag, html_code = self.visitor.generate_html(code)
            if flag:
                self.Editor.setHtml(html_code)
        except Exception:
            self.restoreWindow()
            self.timer.stop()
            return
        self.restoreWindow()
        self.timer.stop()

        word, flag = self.readWordBeforeCursor()
        func_def = self.visitor.search_funcs(word, flag)
        if func_def == "":
            self.ShowDef.setHtml(
                "<p style=\"color:gray\">No definition found</p>")
        else:
            self.ShowDef.setHtml(func_def)

        if word.strip() != "":
            var_list = self.visitor.search_name(word)
            self.ShowVar.reset()
            self.string_list.setStringList(var_list)
        else:
            self.ShowVar.reset()
            self.string_list.setStringList([])


if __name__ == "__main__":
    os.system('antlr4py Python.g4')
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = PythonEditor()
    window.show()
    sys.exit(app.exec_())
