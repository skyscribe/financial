#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import QAbstractTableModel
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL
import operator
import json
import codecs

def createDataModel(mode):
    ''' create a new data model based on given mode'''
    if mode == 'personal':
        return DetailedDataModel()
    else:
        raise Exception("Undefined model for mode %s"%mode)

###############################################################################
class DetailedDataModel(QAbstractTableModel): 
    def __init__(self, parent=None, *args): 
        """ 
        load data from data.json
        """
        QAbstractTableModel.__init__(self, parent, *args) 
        self.dataFile = "data.json"
        self._jsonData = json.load(codecs.getreader('utf-8')(open(self.dataFile)))
        self.header = [u'标记', u'名字', u'分类', u'价格', u'时间', u'备注', u'图片']

        dataArray = []
        for data in self._jsonData:
            id, info = data['id'], data['contents']
            dataArray.append([id, info['name'], info['type'], info['price'], 
                info['date'], info['comments'], info['pic'] ])
        self.dataArray = dataArray

        self.defaultData = [1, u'name', u'type', u'price', u'time', u'comments', u'pics']

    def rowCount(self, parent): 
        return len(self.dataArray) 

    def columnCount(self, parent): 
        return len(self.dataArray[0]) 

    def getPicRowIndex(self):
        return len(self.header) - 1

    def data(self, index, role = Qt.DisplayRole): 
        if not index.isValid(): 
            return QVariant() 
        elif role != Qt.DisplayRole: 
            return QVariant() 
        return QVariant(self.dataArray[index.row()][index.column()]) 

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header[col])
        return QVariant()

    def updateWholeRow(self, row, itemData):
        '''Update whole role using given itemData'''
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        for value in itemData:
            col = itemData.index(value)
            self.dataArray[row][col] = unicode(value)
        self.emit(SIGNAL("layoutChanged()"))
        #Data would be saved upon exit
        #self.saveData()

    def insertRows(self, row, cnt, parent):
        self.beginInsertRows(parent, row, row + cnt - 1)
        for i in range(0, cnt):
            self.dataArray.insert(row, self.defaultData)
        self.endInsertRows()
        return True

    def removeRows(self, row, cnt, parent):
        self.beginRemoveRows(parent, row, row + cnt - 1)
        for i in range(0, cnt):
            self.dataArray.pop(row + i)
        self.endRemoveRows()
        return True

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.dataArray = sorted(self.dataArray, key=operator.itemgetter(Ncol))        
        if order == Qt.DescendingOrder:
            self.dataArray.reverse()
        self.emit(SIGNAL("layoutChanged()"))

    def saveData(self):
        '''Save data to json file'''
        print "saving data..."
        jsonArray = []
        for record in self.dataArray:
            id, name, type, price, date, comments, pic = record
            jsonArray.append({
                    'id' : id,
                    'contents' : {
                        'type'     : type,
                        'date'     : date,
                        'name'     : name,
                        'pic'      : pic,
                        'price'    : price,
                        'comments' : comments
                    }})
        json.dump(jsonArray, codecs.getwriter('utf-8')(open(self.dataFile, "w")),
                indent = 4)

