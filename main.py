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
from EditDlg import CATEGORY_IN
from EditDlg import CATEGORY_OUT
import sys

###############################################################################
class MainApp(QMainWindow):
    modes = [u'总帐目', u'个人帐']
    MODE_TOTAL, MODE_PERSONAL = [0,1]
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self._initMenu()
        self._initData()
        self._bindSignals()
        self._setInitialShow()

    def _initMenu(self):
        fileMenu = self.menuBar().addMenu(u'文件')
        menuOpen = fileMenu.addAction(u'打开历史文件')
        menuExit = fileMenu.addAction(u'退出...')
        menuExit.triggered.connect(self._exit)
        menuExitEx = fileMenu.addAction(u'退出并取消本次所有改动')
        dataMenu = self.menuBar().addMenu(u'数据')
        dataMenu.addAction('导出...')
        aboutMenu = self.menuBar().addMenu(u'关于')

    def _exit(self):
        self.setStatusMsg(u"正在保存数据......");
        self.saveAndFlushData()
        self.close()

    def _initData(self):
        '''Initialize the data'''
        self.ui.modeSelector.addItems(self.modes)     
        self._infoTxt = u'';
        self.ui.btnModify.setDisabled(True)
        self.ui.btnDel.setDisabled(True)

    def _bindSignals(self):
        #self.ui.listData.clicked.connect(self._showCurrentPicture)
        self.ui.btnAdd.clicked.connect(self._addRecord)
        self.ui.btnModify.clicked.connect(self._modifyRecord)
        self.ui.btnDel.clicked.connect(self._delRecords)
        self.ui.listData.doubleClicked.connect(self._modifyRecord)
        self.ui.modeSelector.currentIndexChanged.connect(self._updateSummaryInfo)

    def _setInitialShow(self):
        ''' Set initial data show and styles'''
        model = createDataModel()
        self.ui.listData.setModel(model)
        self.ui.listData.selectionModel().selectionChanged.connect(self._selectionChanged)
        self.ui.pictureShow.setText(u'请选择一列以显示图片')

        self.statusBar().setStyleSheet('background:#33FF99')
        if model.rowCount(None) > 0:
            self.setStatusMsg(u'选择一行或多行修改/删除数据')
            self._updateSummaryInfo()
        else:
            self.setStatusMsg(u'还没有数据，请点击增加新记录添加数据')

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
        self._updateSummaryInfo()
            

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
            if len(rows) == 1:
                self.ui.btnModify.setEnabled(len(rows) == 1)
                self._showCurrentPicture(newSelRow)
                self._updateSummaryInfo()
            self.ui.btnDel.setEnabled(True)
            self.ui.modeSelector.setCurrentIndex(self.MODE_PERSONAL)
        else:
            #enable new, disable del/modify
            self.ui.btnAdd.setEnabled(True)
            self.ui.btnModify.setDisabled(True)
            self.ui.btnDel.setDisabled(True)
            self.ui.pictureShow.setText(u'请选择一行以显示图片')
            self.ui.modeSelector.setCurrentIndex(self.MODE_TOTAL)

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

    def _updateSummaryInfo(self):
        ''' update the summary text '''
        curMode = self.ui.modeSelector.currentIndex() 
        actions = {
                self.MODE_TOTAL: self._showOverall,
                self.MODE_PERSONAL: self._showPersonal
                }
        if actions[curMode]():
            self.ui.summaryInfo.setText(self._infoTxt)


    def _showOverall(self):
        self._infoTxt = u'进货信息合计\n'
        statsIn = self.ui.listData.model().getStatistic(cat = CATEGORY_IN)
        self._infoTxt += getSummaryFromStats(statsIn)
        self._infoTxt += u'\n#####################\n\n'
        self._infoTxt += u'出货信息合计\n'
        statsOut = self.ui.listData.model().getStatistic(cat = CATEGORY_OUT)
        self._infoTxt += getSummaryFromStats(statsOut)
        return True

    def _showPersonal(self):
        data = self.ui.listData
        rows = [selected.row() for selected in data.selectionModel().selectedRows()]
        if len(rows) == 0:
            self.setStatusMsg(u"必须选中某个人才能显示个人统计信息", 1000)
            self.ui.modeSelector.setCurrentIndex(self.MODE_TOTAL)
            return False
        else:
            model = data.model()
            self._infoTxt = u'个人信息统计 [%s - %s]\n'%(model.getName(rows[0]), u'出货')
            stats = data.model().getStatistic(rows[0], CATEGORY_OUT)
            self._infoTxt += getSummaryFromStats(stats)
            self._infoTxt += u'\n#####################\n\n'
            self._infoTxt += u'个人信息统计 [%s - %s]\n'%(model.getName(rows[0]), u'进货')
            stats = data.model().getStatistic(rows[0], CATEGORY_IN)
            self._infoTxt += getSummaryFromStats(stats)
            return True

    def setStatusMsg(self, msg, timeout = 0):
        ''' set status hints'''
        self.statusBar().showMessage(msg, timeout)


def getSummaryFromStats(stats):
    result = u''
    for (k,v) in stats.items():
        result += u'\t%6s => %8d\n'%(k,v)
    result += u'\t---------------------------------\n'
    result += u'\t%6s => %8d\n'%(u'总计', sum([stat for stat in stats.values()]))
    return result

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MainApp()
    myapp.show()
    ret = app.exec_()
    #myapp.saveAndFlushData()
    sys.exit(ret)

