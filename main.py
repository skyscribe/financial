#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mainForm import Ui_MainWindow
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QMainWindow

from DataController import MyTableModel
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
        self.dataFile = "data.json"

        self._initData()
        self._bindSignals()
        self._showDataInList()

    def _initData(self):
        '''Initialize the data'''
        names = [v for (k,v) in self.modes.items()]
        names.sort()
        self.ui.modeSelector.addItems(names)     
        self._loadJsonData()

    def _loadJsonData(self):
        import json
        import codecs
        self._jsonData = json.load(codecs.getreader('utf-8')(open('data.json')))

    def _bindSignals(self):
        self.ui.listData.clicked.connect(self._showCurrentPicture)

    def _showDataInList(self):
        ''' Show the data in list by mode'''
        mode = self._getSelectedMode()
        if mode == 'personal':
            self._showDataInDetailedMode()

    def _showDataInDetailedMode(self):
        header = [u'标记', u'名字', u'分类', u'价格', u'备注', u'图片']
        dataForList = []
        for data in self._jsonData:
            id, info = data['id'], data['contents']
            dataForList.append([id, info['name'], info['type'], info['price'], 
                info['comments'], info['pic'] ])

        listData = self.ui.listData
        model = MyTableModel(dataForList, header)
        listData.setModel(model)
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

