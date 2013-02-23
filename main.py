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
        self._setInitialShow()

    def _initData(self):
        '''Initialize the data'''
        names = [v for (k,v) in self.modes.items()]
        names.sort()
        self.ui.modeSelector.addItems(names)     
        self.ui.btnModify.setDisabled(True)
        self.ui.btnDel.setDisabled(True)

    def _bindSignals(self):
        #self.ui.listData.clicked.connect(self._showCurrentPicture)
        self.ui.btnAdd.clicked.connect(self._addRecord)
        self.ui.btnModify.clicked.connect(self._modifyRecord)
        self.ui.btnDel.clicked.connect(self._delRecords)
        self.ui.listData.doubleClicked.connect(self._modifyRecord)

    def _setInitialShow(self):
        ''' Set initial data show and styles'''
        self._mode = self._getSelectedMode()
        model = createDataModel(self._getSelectedMode())
        self.ui.listData.setModel(model)
        self.ui.listData.selectionModel().selectionChanged.connect(self._selectionChanged)
        self.ui.pictureShow.setText(u'请选择一列以显示图片')

        self.statusBar().setStyleSheet('background:#33FF99')
        if model.rowCount(None) > 0:
            self.setStatusMsg(u'选择一行或多行修改/删除数据')
        else:
            self.setStatusMsg(u'还没有数据，请点击增加新记录添加数据')

    def _getSelectedMode(self):
        selectedText = unicode(self.ui.modeSelector.currentText())
        modes = [k for (k,v) in self.modes.items() if v == selectedText ]
        if len(modes) == 0:
            raise Exception(u"Bad mode, current selected text: %s" % selectedText)
        return modes[0]
        

    def saveAndFlushData(self):
        ''' Save and flush the list data '''
        self.ui.listData.model().saveData()

    def _modifyRecord(self):
        dlg = EditDlg(self, 'modify')
        ret = dlg.exec_()

    def _addRecord(self):
        dlg = EditDlg(self, 'add')
        ret = dlg.exec_()

    def _delRecords(self):
        data = self.ui.listData
        rows = [selected.row() for selected in data.selectionModel().selectedRows()]
        result = [str(row) for row in rows if data.model().removeRow(row)]
        self.setStatusMsg(u"成功删除了%d行数据，行号:%s"%(len(result), ','.join(result)), 2000)
            

    def _selectionChanged(self, selected, deselected):
        getRow = lambda sel : len(sel.indexes()) != 0 and sel.indexes()[0].row or (-1)
        newSelRow = getRow(selected)
        oldSelRow = getRow(deselected)
        if newSelRow != -1:
            data = self.ui.listData
            rows = [selected.row() for selected in data.selectionModel().selectedRows()]
            rows.sort()
            rows = [str(id) for id in rows]
            self.setStatusMsg(u"选择了如下行:%s"%(','.join(rows)), 2000)
            #enable del/modify, disable new
            self.ui.btnAdd.setDisabled(True)
            self.ui.btnModify.setEnabled(len(rows) == 1)
            self.ui.btnDel.setEnabled(True)
            self._showCurrentPicture(newSelRow)
        else:
            #enable new, disable del/modify
            self.ui.btnAdd.setEnabled(True)
            self.ui.btnModify.setDisabled(True)
            self.ui.btnDel.setDisabled(True)
            self.ui.pictureShow.setText(u'请选择一行以显示图片')

    def _showCurrentPicture(self, selRow):
        '''Show current selected item's picture'''
        selRow = selRow()
        model = self.ui.listData.model()
        picPath = model.data(model.createIndex(selRow, model.getPicRowIndex())).toString()
        #self.ui.pictureShow.setText(u'选择了第%d列, 地址为:%s'%(selRow, picData))
        #TODO: using QPixelMap to load and show the image for correct scale

        picShow = self.ui.pictureShow
        pixmap = QPixmap(picPath)
        if pixmap.isNull():
            picShow.setText(u'第%d行数据对应的图片\n[%s]\n\n无法加载显示！'%(selRow, picPath))
        else:
            rect = picShow.frameRect()
            pixmap.scaled(rect.width(), rect.height(), Qt.KeepAspectRatioByExpanding)
            self.ui.pictureShow.setPixmap(pixmap)

    def setStatusMsg(self, msg, timeout = 0):
        ''' set status hints'''
        self.statusBar().showMessage(msg, timeout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MainApp()
    myapp.show()
    ret = app.exec_()
    myapp.saveAndFlushData()
    sys.exit(ret)

