#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QFileDialog
from PyQt4.QtCore import QDateTime

from modify import Ui_EditDlg
import os.path

class EditDlg(QDialog):
    def __init__(self, parent, mode):
        QWidget.__init__(self, parent)
        self.ui = Ui_EditDlg()
        self.ui.setupUi(self)
        self.listData = parent.ui.listData

        self.ui.btnChooser.clicked.connect(self._chooseFile)
        
        if mode == 'add':
            self._prepForAdd()
        else:
            self._prepForModify()


    def _prepForAdd(self):
        model = self.listData.model()
        #Load id
        newId = model.rowCount(None) + 1
        self.ui.editID.setText(str(newId))
        #Set current time
        self.ui.editTime.setDateTime(QDateTime.currentDateTime())

    def _prepForModify(self):
        model = self.listData.model()
        selected = self.listData.selectedIndexes()[0]
        row = selected.row()
        fetchValue = lambda col: model.data(model.createIndex(row, col)).toString()
        self.ui.editID.setText(fetchValue(0))
        self.ui.editName.setText(fetchValue(1))
        self.ui.editType.setText(fetchValue(2))
        self.ui.editPrice.setText(fetchValue(3))
        self.ui.editTime.setDateTime(QDateTime.currentDateTime())
        self.ui.editComments.setText(fetchValue(5))
        self.ui.editPic.setText(fetchValue(6))
 
    def accept(self):
        print "accepted!"

    def reject(self):
        print "rejected!"
        

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
