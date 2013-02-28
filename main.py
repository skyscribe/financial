#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DataController import createDataModel
from EditDlg import CATEGORY_IN
from EditDlg import CATEGORY_OUT
from EditDlg import EditDlg
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QWidget
from mainForm import Ui_MainWindow
import os
import sys
import codecs

###############################################################################
class MainApp(QMainWindow):
    modes = [u'总帐目', u'个人帐']
    MODE_TOTAL, MODE_PERSONAL = [0,1]
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self._initDirectories()
        self._initMenu()
        self._initData()
        self._bindSignals()

    def _initDirectories(self):
        for dir in [u'图片库', u'历史数据', u'数据']:
            if not os.access(dir, os.F_OK):
                os.mkdir(dir)

    def _initMenu(self):
        fileMenu = self.menuBar().addMenu(u'文件')
        for fileName in  sorted([(u'历史数据' + os.path.sep + fname) for fname in os.listdir(u'历史数据') \
                    if fname.startswith('data.') and fname.endswith('.json') \
                ], reverse = True)[:10]:
            subMenu = fileMenu.addAction(unicode(fileName))
            subMenu.triggered.connect(lambda:self._initListData(fileName))
        subMenu = fileMenu.addAction(u'选择历史文件...')
        subMenu.triggered.connect(self._selectFile)

        menuExit = fileMenu.addAction(u'退出...')
        menuExit.triggered.connect(lambda: self._exit(True))
        menuExitEx = fileMenu.addAction(u'退出并取消本次所有改动')
        menuExitEx.triggered.connect(lambda: self._exit(False))

        dataMenu = self.menuBar().addMenu(u'数据')
        subMenu = dataMenu.addAction(u'导出...')
        subMenu.triggered.connect(self._export)
        aboutMenu = self.menuBar().addMenu(u'关于')

    def _initListData(self, fileName = './data.json'):
        self._currentFile = fileName
        model = createDataModel(fileName)
        self.ui.listData.setModel(model)
        self.ui.listData.selectionModel().selectionChanged.connect(self._selectionChanged)
        self.setStatusMsg(u'文件 [%s] 已经加载'%fileName)
        self._flushDisplay()

    def _selectFile(self):
        '''select file from history'''
        chooser = QFileDialog(self, u"选择一个文件", "history", "*.json")
        chooser.setModal(True)
        if chooser.exec_():
            self._initListData(chooser.selectedFiles()[0])

    def _exit(self, saveData = True):
        if saveData:
            self.setStatusMsg(u"正在保存数据......");
            self.saveAndFlushData()
        self.close()
        self.saveData = saveData

    def _export(self):
        chooser = QFileDialog(self, u"输入文件名", u'数据')
        chooser.setModal(True)
        if chooser.exec_():
            fpath = unicode(chooser.selectedFiles()[0])
            if not fpath.endswith(u'csv'):
                fpath += u'.csv'
            fout = codecs.getwriter('utf-8')(open(fpath, "w"))
            self.ui.listData.model().dumpData(fout)


    def _initData(self):
        '''Initialize the data during startup'''
        self.ui.modeSelector.addItems(self.modes)     
        self._infoTxt = u'';
        self.ui.btnModify.setDisabled(True)
        self.ui.btnDel.setDisabled(True)
        self._initListData()
        self._hasDataChanges = False

    def _bindSignals(self):
        self.ui.btnAdd.clicked.connect(self._addRecord)
        self.ui.btnModify.clicked.connect(self._modifyRecord)
        self.ui.btnDel.clicked.connect(self._delRecords)
        self.ui.listData.doubleClicked.connect(self._modifyRecord)
        self.ui.modeSelector.currentIndexChanged.connect(self._updateSummaryInfo)

    def _flushDisplay(self):
        ''' Set initial data show and styles'''
        self.ui.pictureShow.setText(u'请选择一列以显示图片')
        self.statusBar().setStyleSheet('background:#33FF99')
        if self.ui.listData.model().rowCount(None) > 0:
            self.setStatusMsg(u'选择一行或多行修改/删除数据')
            self._updateSummaryInfo()
        else:
            self.setStatusMsg(u'当前文件[%s]还没有数据，请点击增加新记录添加数据'%self._currentFile)

    def saveAndFlushData(self, fname = 'data.json'):
        ''' Save and flush the list data '''
        #print "Saving data into file %s"%fname
        if self._hasDataChanges:
            self.ui.listData.model().saveData(fname)
        else:
            print "Nothing to update!"

    def _modifyRecord(self):
        dlg = EditDlg(self, 'modify')
        dlg.exec_()
        if dlg.hasUpdates:
            self._hasDataChanges = True

    def _addRecord(self):
        dlg = EditDlg(self, 'add')
        dlg.exec_()
        if dlg.hasUpdates:
            self._hasDataChanges = True

    def _delRecords(self):
        data = self.ui.listData
        rows = [selected.row() for selected in data.selectionModel().selectedRows()]
        result = [str(row) for row in rows if data.model().removeRow(row)]
        self.setStatusMsg(u"成功删除了%d行数据，行号:%s"%(len(result), ','.join(result)), 2000)
        self._hasDataChanges = True
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
        infoTxt = u''
        delimiter = u'\n#####################\n\n'
        statsIn = self.ui.listData.model().getStatistic(cat = CATEGORY_IN)
        statsOut = self.ui.listData.model().getStatistic(cat = CATEGORY_OUT)
        infoTxt += getSummaryText(u'进货信息合计\n', statsIn, delimiter)
        infoTxt += getSummaryText(u'出货信息合计\n', statsOut, delimiter)
        infoTxt += getSummaryText(u'净资金分类信息\n', getAbsStats(statsIn, statsOut), u'')
        self._infoTxt = infoTxt
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
            txt = u''
            statsOut = data.model().getStatistic(rows[0], CATEGORY_OUT)
            statsIn = data.model().getStatistic(rows[0], CATEGORY_IN)
            txt += getSummaryText(u'个人信息统计 [%s - %s]\n'%(model.getName(rows[0]), u'出货'),
                    statsOut, u'\n#####################\n\n') 
            txt += getSummaryText(u'个人信息统计 [%s - %s]\n'%(model.getName(rows[0]), u'进货'),
                    statsOut, u'\n#####################\n\n')
            txt += getSummaryText(u'净资金分类信息\n', getAbsStats(statsIn, statsOut), u'')
            self._infoTxt = txt
            return True

    def setStatusMsg(self, msg, timeout = 0):
        ''' set status hints'''
        self.statusBar().showMessage(msg, timeout)

    def isViewingHistoryFile(self):
        return self._currentFile.startswith(u'历史数据')

def getAbsStats(statsIn, statsOut):
    stats = {}
    types = statsIn.keys()
    types.extend(statsOut.keys())
    for k in types:
        stats[k] = 0
        if statsOut.has_key(k):
            stats[k] += statsOut[k]
        if statsIn.has_key(k):
            stats[k] -= statsIn[k]
    return stats

def getSummaryText(prefix, stats, suffix):
    return prefix + getSummaryFromStats(stats) + suffix

def getSummaryFromStats(stats):
    result = u''
    for k in sorted(stats.keys()):
        result += u'\t%6s => %8d\n'%(k, stats[k])
    result += u'\t---------------------------------\n'
    result += u'\t%6s => %8d\n'%(u'总计', sum([stat for stat in stats.values()]))
    return result

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MainApp()
    myapp.show()
    ret = app.exec_()
    if not hasattr(myapp, 'saveData') and not myapp.isViewingHistoryFile():
        print "save data implicitly..."
        myapp.saveAndFlushData()
    sys.exit(ret)
