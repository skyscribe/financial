#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QFileDialog
from PyQt4.QtCore import QDateTime

from modify import Ui_EditDlg
import os.path

categories = [u'进货', u'出货']
CATEGORY_IN, CATEGORY_OUT = [0,1]

class EditDlg(QDialog):
    def __init__(self, parent, mode):
        QWidget.__init__(self, parent)
        self.ui = Ui_EditDlg()
        self.ui.setupUi(self)
        self.listData = parent.ui.listData
        self.setStatusMsg = parent.setStatusMsg
        self.mode = mode
        self._hasUpdates = False

        self.ui.comboCategory.addItems(categories)
        self.ui.comboCategory.setCurrentIndex(0);
        self.ui.btnChooser.clicked.connect(self._chooseFile)

        if mode == 'add':
            self._prepForAdd()
        else:
            self._prepForModify()

        #Listen for changes after preparation
        for ctrl in ['editName', 'editType', 'editPrice', 'editPic', 'editComments']:
            getattr(self.ui, ctrl).textChanged.connect(self._dataChanged)
        self.ui.comboCategory.currentIndexChanged.connect(self._dataChanged)

    def _dataChanged(self):
        print "data changed!"
        self._hasUpdates = True

    def _prepForAdd(self):
        model = self.listData.model()
        #Load id
        self.ui.editID.setText(str(model.getNewUnusedId()))
        self.ui.comboCategory.setCurrentIndex(0)
        #Set current time
        self.ui.editTime.setDateTime(QDateTime.currentDateTime())

    def _prepForModify(self):
        model = self.listData.model()
        selected = self.listData.selectedIndexes()[0]
        row = selected.row()
        fetchByColId = lambda col: model.data(model.createIndex(row, col)).toString()
        fetchColId = lambda name: model.getColIndexByName(name)
        fetchValue = lambda name: fetchByColId(fetchColId(name))
        self.ui.editID.setText(fetchValue('ID'))
        self.ui.editName.setText(fetchValue('Name'))
        self.ui.editType.setText(fetchValue('Type'))
        self.ui.editPrice.setText(fetchValue('Price'))
        dt = QDateTime.fromString(fetchValue('Time'), "yyyy-MM-dd HH:mm:ss")
        if not dt.isValid():
            dt = QDateTime.currentDateTime()
        self.ui.editTime.setDateTime(dt)
        self.ui.editComments.setText(fetchValue('Comments'))
        self.ui.editPic.setText(fetchValue('Pic'))

        catMatches = [k for k in categories if fetchValue('Category') == k]
        if len(catMatches) == 0:
            self.ui.comboCategory.setCurrentIndex(0)
        else:
            self.ui.comboCategory.setCurrentIndex(categories.index(catMatches[0]))
 
    def accept(self):
        '''Accept the changes'''
        self.setStatusMsg(u'添加/修改无变化，已自动撤销', 3000)
        if not self._hasUpdates:
            return True

        model = self.listData.model()
        if self.mode == 'add':
            model.insertRow(model.rowCount(None))
            row = model.rowCount(None) - 1
            self.setStatusMsg(u'添加新交易已经成功，目前总共 %d 条记录'%(row + 1))
        else:
            self.ui.editTime.setDateTime(QDateTime.currentDateTime())
            row = self.listData.selectedIndexes()[0].row()
            self.setStatusMsg(u'修改记录已经成功', 3000)

        getEditText = lambda name: getattr(self.ui, name).toPlainText()
        getColTag = lambda tagName : model.getColTagByName(tagName)
        itemData = {
            getColTag('ID')       : getEditText('editID'),
            getColTag('Name')     : getEditText('editName'),
            getColTag('Type')     : getEditText('editType'),
            getColTag('Price')    : getEditText('editPrice'),
            getColTag('Time')     : self.ui.editTime.dateTime().toString("yyyy-MM-dd HH : mm : ss"),
            getColTag('Comments') : getEditText('editComments'),
            getColTag('Pic')      : getEditText('editPic'),
            getColTag('Category') : self.ui.comboCategory.currentText(), 
            }
        model.updateWholeRow(row, itemData)
        return True
        
    def reject(self):
        return False
        

    def _chooseFile(self):
        chooser = QFileDialog(self, u"选择一个图片", "./", "*.jpg")
        chooser.setModal(True)
        if chooser.exec_():
            file_choosed = unicode(chooser.selectedFiles()[0])
            fpath = unicode(os.path.sep).join([u"pictures", file_choosed.split(os.path.sep)[-1] ])
            print fpath
            if not os.access(fpath, os.F_OK):
                with open(fpath, 'wb') as ofh:
                    with open(file_choosed, 'rb') as ifh:
                        for line in ifh:
                            ofh.write(line)
            self.ui.editPic.setText(fpath)

