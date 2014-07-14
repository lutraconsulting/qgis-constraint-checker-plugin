# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_constraint_results.ui'
#
# Created: Tue Mar 25 14:25:46 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(800, 600)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)
        self.constraintTableView = QtGui.QTableView(Dialog)
        self.constraintTableView.setObjectName(_fromUtf8("constraintTableView"))
        self.gridLayout.addWidget(self.constraintTableView, 0, 0, 1, 2)
        self.exportToCSVPushButton = QtGui.QPushButton(Dialog)
        self.exportToCSVPushButton.setMinimumSize(QtCore.QSize(90, 0))
        self.exportToCSVPushButton.setObjectName(_fromUtf8("exportToCSVPushButton"))
        self.gridLayout.addWidget(self.exportToCSVPushButton, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QObject.connect(self.exportToCSVPushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.export)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Constraint Results", None, QtGui.QApplication.UnicodeUTF8))
        self.exportToCSVPushButton.setText(QtGui.QApplication.translate("Dialog", "Export to CSV", None, QtGui.QApplication.UnicodeUTF8))

