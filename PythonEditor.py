# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PythonEditor.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PythonEditor(object):
    def setupUi(self, PythonEditor):
        PythonEditor.setObjectName("PythonEditor")
        PythonEditor.resize(1250, 790)
        PythonEditor.setMinimumSize(QtCore.QSize(1250, 790))
        self.centralwidget = QtWidgets.QWidget(PythonEditor)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.CommandBar = CommandBar(self.centralwidget)
        self.CommandBar.setMinimumSize(QtCore.QSize(155, 30))
        self.CommandBar.setMaximumSize(QtCore.QSize(155, 30))
        self.CommandBar.setObjectName("CommandBar")
        self.gridLayout.addWidget(self.CommandBar, 0, 2, 1, 1)
        self.ShowDef = TextEdit(self.centralwidget)
        self.ShowDef.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(False)
        self.ShowDef.setFont(font)
        self.ShowDef.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ShowDef.setReadOnly(True)
        self.ShowDef.setObjectName("ShowDef")
        self.gridLayout.addWidget(self.ShowDef, 0, 1, 1, 1)
        self.ShowVar = ListView(self.centralwidget)
        self.ShowVar.setObjectName("ShowVar")
        self.gridLayout.addWidget(self.ShowVar, 0, 0, 1, 1)
        self.Editor = TextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        self.Editor.setFont(font)
        self.Editor.setObjectName("Editor")
        self.gridLayout.addWidget(self.Editor, 1, 0, 1, 3)
        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 6)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 6)
        PythonEditor.setCentralWidget(self.centralwidget)

        self.retranslateUi(PythonEditor)
        QtCore.QMetaObject.connectSlotsByName(PythonEditor)

    def retranslateUi(self, PythonEditor):
        _translate = QtCore.QCoreApplication.translate
        PythonEditor.setWindowTitle(_translate("PythonEditor", "Python Editor"))
        self.Editor.setHtml(_translate("PythonEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\',\'Microsoft YaHei\',\'PingFang SC\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
from qfluentwidgets import CommandBar, ListView, TextEdit