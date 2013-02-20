# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainForm.ui'
#
# Created: Wed Feb 20 22:47:41 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(946, 629)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 101, 21))
        self.label_2.setStyleSheet(_fromUtf8("color: green"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.modeSelector = QtGui.QComboBox(self.centralwidget)
        self.modeSelector.setGeometry(QtCore.QRect(210, 20, 451, 27))
        self.modeSelector.setStyleSheet(_fromUtf8("background:rgb(0, 255, 255);\n"
"color: rgb(170, 0, 255);"))
        self.modeSelector.setObjectName(_fromUtf8("modeSelector"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 50, 641, 551))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.listData = QtGui.QTableView(self.layoutWidget)
        self.listData.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
        self.listData.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.listData.setShowGrid(True)
        self.listData.setSortingEnabled(True)
        self.listData.setObjectName(_fromUtf8("listData"))
        self.listData.horizontalHeader().setDefaultSectionSize(100)
        self.verticalLayout.addWidget(self.listData)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnPrevious = QtGui.QPushButton(self.layoutWidget)
        self.btnPrevious.setObjectName(_fromUtf8("btnPrevious"))
        self.horizontalLayout.addWidget(self.btnPrevious)
        self.btnAdd = QtGui.QPushButton(self.layoutWidget)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.horizontalLayout.addWidget(self.btnAdd)
        self.btnNext = QtGui.QPushButton(self.layoutWidget)
        self.btnNext.setObjectName(_fromUtf8("btnNext"))
        self.horizontalLayout.addWidget(self.btnNext)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(670, 20, 261, 21))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName(_fromUtf8("label"))
        self.pictureShow = QtGui.QLabel(self.centralwidget)
        self.pictureShow.setGeometry(QtCore.QRect(670, 50, 261, 251))
        self.pictureShow.setFrameShape(QtGui.QFrame.StyledPanel)
        self.pictureShow.setText(_fromUtf8(""))
        self.pictureShow.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.pictureShow.setObjectName(_fromUtf8("pictureShow"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.modeSelector.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.modeSelector, self.listData)
        MainWindow.setTabOrder(self.listData, self.btnPrevious)
        MainWindow.setTabOrder(self.btnPrevious, self.btnAdd)
        MainWindow.setTabOrder(self.btnAdd, self.btnNext)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "记账/查看工具", None, QtGui.QApplication.UnicodeUTF8))
        MainWindow.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p>这是一个简单的几张查看/添加工具</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        MainWindow.setWhatsThis(QtGui.QApplication.translate("MainWindow", "简单记账管理工具", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "选择显示类型", None, QtGui.QApplication.UnicodeUTF8))
        self.btnPrevious.setText(QtGui.QApplication.translate("MainWindow", "上一页", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAdd.setText(QtGui.QApplication.translate("MainWindow", "增加新记录", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNext.setText(QtGui.QApplication.translate("MainWindow", "下一页", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "图片显示", None, QtGui.QApplication.UnicodeUTF8))

