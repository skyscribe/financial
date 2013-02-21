#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mainForm import Ui_MainWindow
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QMainWindow

from DataController import createDataModel
import sys

###############################################################################
class MainApp(QMainWindow):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Constant info
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

    def _bindSignals(self):
        self.ui.listData.clicked.connect(self._showCurrentPicture)

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
        selected = self.ui.listData.selectedIndexes()[0]
        row = selected.row()
        model = self.ui.listData.model()
        picData = model.data(model.createIndex(row, 5)).toString()
        self.ui.pictureShow.setText(u'选择了第%d列, 地址为:%s'%(row, picData))
        #TODO: using QPixelMap to load and show the image for correct scale


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MainApp()
    myapp.show()
    sys.exit(app.exec_())

