#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DataController import createDataModel

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QWidget

from mainForm import Ui_MainWindow
from EditDlg import EditDlg
import sys

###############################################################################
class MainApp(QMainWindow):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Constant infoG
        self.modes = {
        "totalIn" : u'总帐目-出货',
        "totalOut" : u'总帐目 - 进货',
        "personal" : u'个人帐', 
        }

        self._initData()
        self._bindSignals()
        self._showDataInList()

    def _initData(self):
        '''Initialize the data'''
        names = [v for (k,v) in self.modes.items()]
        names.sort()
        self.ui.modeSelector.addItems(names)     
        self.ui.btnModify.setDisabled(True)
        self.ui.btnDel.setDisabled(True)

    def _bindSignals(self):
        self.ui.listData.clicked.connect(self._showCurrentPicture)
        self.ui.btnAdd.clicked.connect(self._addRecord)
        self.ui.btnModify.clicked.connect(self._modifyRecord)
        self.ui.listData.doubleClicked.connect(self._modifyRecord)

    def _showDataInList(self):
        ''' Show the data in list by mode'''
        self._mode = self._getSelectedMode()
        model = createDataModel(self._getSelectedMode())
        self.ui.listData.setModel(model)
        #[listData.setColumnWidth(i, listData.columnWidth(i)*2) for i in range(len(header)-2, len(header)) ]

    def _getSelectedMode(self):
        selectedText = unicode(self.ui.modeSelector.currentText())
        modes = [k for (k,v) in self.modes.items() if v == selectedText ]
        if len(modes) == 0:
            raise Exception(u"Bad mode, current selected text: %s" % selectedText)
        return modes[0]
        

    def _showCurrentPicture(self):
        '''Show current selected item's picture'''
        selected = self.ui.listData.selectedIndexes()[0]
        row = selected.row()
        model = self.ui.listData.model()
        picPath = model.data(model.createIndex(row, model.getPicRowIndex())).toString()
        #self.ui.pictureShow.setText(u'选择了第%d列, 地址为:%s'%(row, picData))
        #TODO: using QPixelMap to load and show the image for correct scale

        picShow = self.ui.pictureShow
        pixmap = QPixmap(picPath)
        if pixmap.isNull():
            picShow.setText(u'第%d行数据对应的图片\n[%s]\n\n无法加载显示！'%(row, picPath))
        else:
            rect = picShow.frameRect()
            pixmap.scaled(rect.width(), rect.height(), Qt.KeepAspectRatioByExpanding)
            self.ui.pictureShow.setPixmap(pixmap)

        #Enable other 2 buttons
        self.ui.btnModify.setEnabled(True)
        self.ui.btnDel.setEnabled(True)

    def _saveAndFlushData(self):
        ''' Save and flush the list data '''
        self.ui.listData.model().saveData()

    def _modifyRecord(self):
        dlg = EditDlg(self, 'modify')
        ret = dlg.exec_()

    def _addRecord(self):
        dlg = EditDlg(self, 'add')
        ret = dlg.exec_()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MainApp()
    myapp.show()
    sys.exit(app.exec_())

