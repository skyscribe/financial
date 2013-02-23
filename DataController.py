#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import QAbstractTableModel
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL
from EditDlg import categories
import operator
import json
import codecs

def createDataModel():
    ''' create a new data model'''
    return DetailedDataModel()

###############################################################################
class DetailedDataModel(QAbstractTableModel): 
    def __init__(self, parent=None, *args): 
        """ 
        load data from data.json
        """
        QAbstractTableModel.__init__(self, parent, *args) 
        self.dataFile = "data.json"
        self._jsonData = json.load(codecs.getreader('utf-8')(open(self.dataFile)))
        self.header = [u'标记', u'名字', u'分类', u'进/出货', u'价格', u'时间', u'备注', u'图片']
        self.headerLiteral = ['ID', 'Name', 'Type', 'Category', 'Price', 'Time', 'Comments', 'Pic']

        dataArray = []
        for data in self._jsonData:
            id, info = data['id'], data['contents']
            dataArray.append([id, info['name'], info['type'], info['category'], info['price'], 
                info['date'], info['comments'], info['pic'] ])
        self.dataArray = dataArray

        self.defaultData = [1, u'name', u'type', u'cat', u'price', u'time', u'comments', u'pics']

    def getColIndexByName(self, name):
        return self.headerLiteral.index(name)

    def getColTagByName(self, name):
        return self.header[self.headerLiteral.index(name)]

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
        '''
        Update whole role using given itemData, data shall in format of
        '''
        #print "====Before update, rows:"
        #self.dumpData(sys.stdout)
        self.emit(SIGNAL("layoutChanged()"))
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        print "updating row:%d"%row
        for (tag, value) in itemData.items():
            col = self.header.index(tag)
            self.dataArray[row][col] = unicode(value)
            print u'setting array[%d][%d] to %s'%(row, col, value)

        #print "@@@@@@After update, rows:"
        #self.dumpData(sys.stdout)
        self.emit(SIGNAL("layoutChanged()"))

    def insertRows(self, row, cnt, parent):
        self.beginInsertRows(parent, row, row + cnt - 1)
        #self.dumpData(sys.stdout, "###### Before insert, rows:")
        for i in range(0, cnt):
            if row < len(self.dataArray):
                self.dataArray.insert(row, list(self.defaultData))
            else:
                self.dataArray.append(list(self.defaultData))
        #self.dumpData(sys.stdout, "----- After insert, rows:")
        self.endInsertRows()
        return True

    def removeRows(self, row, cnt, parent):
        self.beginRemoveRows(parent, row, row + cnt - 1)
        for i in range(cnt-1, -1, -1):
            if (row + i) < len(self.dataArray):
                self.dataArray.pop(row + i)
            else:
                pass
                #print "invalid row:%d to remove!"%(row+i)
        self.endRemoveRows()
        return True

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        cmpFunc = None
        if Ncol == self.headerLiteral.index('ID') or Ncol == self.headerLiteral.index('Price'):
            cmpFunc = lambda l,r: (int(l) - int(r))
        self.dataArray = sorted(self.dataArray, key=operator.itemgetter(Ncol), cmp = cmpFunc)        
        if order == Qt.DescendingOrder:
            self.dataArray.reverse()
        self.emit(SIGNAL("layoutChanged()"))

    def saveData(self):
        '''Save data to json file'''
        print "saving data..."
        jsonArray = []
        for record in self.dataArray:
            id, name, type, category, price, date, comments, pic = record
            jsonArray.append({
                    'id' : id,
                    'contents' : {
                        'type'     : type,
                        'category' : category,
                        'date'     : date,
                        'name'     : name,
                        'pic'      : pic,
                        'price'    : price,
                        'comments' : comments
                    }})
        json.dump(jsonArray, codecs.getwriter('utf-8')(open(self.dataFile, "w")),
                indent = 4)

    def getNewUnusedId(self):
        '''choose an unique unused id, for adding'''
        idSet = [ int(str(item[0])) for item in self.dataArray ]
        unusedId = min(list(set(range(1, len(idSet) + 2)) - set(idSet)))
        return unusedId

    def dumpData(self, out, hint = ""):
        if hint != "":
            out.write(hint + "\n")
        rowId = 1
        for row in self.dataArray:
            for col in range(0, len(self.dataArray[0])):
                out.write(u"%s,"%row[col])
            out.write("\n")
            rowId = rowId + 1

    def getName(self, row):
        return self.dataArray[row][self.getColIndexByName('Name')]

    def getCategory(self, row):
        return self.dataArray[row][self.getColIndexByName('Category')]

    def getStatistic(self, selectedRow = -1, cat = -1):
        '''
        return statistics like:
            IN:
                TypeA: 100
                TypeB: 200
                TypeC: 300
        or:
            OUT:
                Type1: 200
                Type2: 400
        '''
        result = {}
        nameCol = self.getColIndexByName('Name')
        catCol = self.getColIndexByName('Category')

        if selectedRow in range(0, len(self.dataArray)):
            name = self.dataArray[selectedRow][nameCol]
        else:
            name = ''
        category = categories[cat]

        nameMatch = lambda data: name == '' and True or data[nameCol] == name
        catMatch = lambda data: category == -1 and True or data[catCol] == category
        filtered = [data for data in self.dataArray if nameMatch(data) and catMatch(data)]

        print "matched count:%d"%len(filtered)
        typeCol = self.getColIndexByName('Type')
        priceCol = self.getColIndexByName('Price')
        types = list(set([data[typeCol] for data in filtered]))
        for type in types:
            result[type] = sum([int(data[priceCol]) for data in filtered if type == data[typeCol] ])
        return result

