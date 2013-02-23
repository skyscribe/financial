# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainForm.ui'
#
# Created: Sat Feb 23 17:49:35 2013
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
        MainWindow.resize(975, 635)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.modeSelector = QtGui.QComboBox(self.centralwidget)
        self.modeSelector.setGeometry(QtCore.QRect(80, 20, 191, 27))
        self.modeSelector.setStyleSheet(_fromUtf8("background:rgb(0, 255, 255);\n"
"color: rgb(170, 0, 255);"))
        self.modeSelector.setObjectName(_fromUtf8("modeSelector"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(290, 20, 671, 581))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.listData = QtGui.QTableView(self.layoutWidget)
        self.listData.setFrameShadow(QtGui.QFrame.Raised)
        self.listData.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
        self.listData.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.listData.setShowGrid(True)
        self.listData.setSortingEnabled(True)
        self.listData.setObjectName(_fromUtf8("listData"))
        self.listData.horizontalHeader().setDefaultSectionSize(100)
        self.verticalLayout.addWidget(self.listData)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnAdd = QtGui.QPushButton(self.layoutWidget)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.horizontalLayout.addWidget(self.btnAdd)
        self.btnDel = QtGui.QPushButton(self.layoutWidget)
        self.btnDel.setObjectName(_fromUtf8("btnDel"))
        self.horizontalLayout.addWidget(self.btnDel)
        self.btnModify = QtGui.QPushButton(self.layoutWidget)
        self.btnModify.setObjectName(_fromUtf8("btnModify"))
        self.horizontalLayout.addWidget(self.btnModify)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 330, 261, 21))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName(_fromUtf8("label"))
        self.pictureShow = QtGui.QLabel(self.centralwidget)
        self.pictureShow.setGeometry(QtCore.QRect(10, 350, 261, 251))
        self.pictureShow.setFrameShape(QtGui.QFrame.StyledPanel)
        self.pictureShow.setText(_fromUtf8(""))
        self.pictureShow.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.pictureShow.setObjectName(_fromUtf8("pictureShow"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 61, 21))
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.summaryInfo = QtGui.QTextBrowser(self.centralwidget)
        self.summaryInfo.setGeometry(QtCore.QRect(10, 60, 261, 261))
        self.summaryInfo.setFrameShape(QtGui.QFrame.StyledPanel)
        self.summaryInfo.setFrameShadow(QtGui.QFrame.Sunken)
        self.summaryInfo.setOpenLinks(False)
        self.summaryInfo.setObjectName(_fromUtf8("summaryInfo"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setStyleSheet(_fromUtf8("background: rgb(0, 255, 127)"))
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.modeSelector.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.modeSelector, self.listData)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "记账/查看工具", None, QtGui.QApplication.UnicodeUTF8))
        MainWindow.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p>这是一个简单的几张查看/添加工具</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        MainWindow.setWhatsThis(QtGui.QApplication.translate("MainWindow", "简单记账管理工具", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAdd.setText(QtGui.QApplication.translate("MainWindow", "增加新记录", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDel.setText(QtGui.QApplication.translate("MainWindow", "删除当前记录", None, QtGui.QApplication.UnicodeUTF8))
        self.btnModify.setText(QtGui.QApplication.translate("MainWindow", "修改记录", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "当前图片", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "汇总信息", None, QtGui.QApplication.UnicodeUTF8))

