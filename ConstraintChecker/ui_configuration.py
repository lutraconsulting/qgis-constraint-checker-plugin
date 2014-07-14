# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_configuration.ui'
#
# Created: Tue Apr 29 19:00:04 2014
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
        Dialog.resize(848, 453)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.postgisConnectionComboBox = QtGui.QComboBox(Dialog)
        self.postgisConnectionComboBox.setObjectName(_fromUtf8("postgisConnectionComboBox"))
        self.gridLayout.addWidget(self.postgisConnectionComboBox, 0, 1, 1, 1)
        self.postgisConnectionLabel = QtGui.QLabel(Dialog)
        self.postgisConnectionLabel.setObjectName(_fromUtf8("postgisConnectionLabel"))
        self.gridLayout.addWidget(self.postgisConnectionLabel, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 3)
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout_2.addWidget(self.tableWidget, 1, 0, 1, 3)
        self.newConstraintPushButton = QtGui.QPushButton(Dialog)
        self.newConstraintPushButton.setObjectName(_fromUtf8("newConstraintPushButton"))
        self.gridLayout_2.addWidget(self.newConstraintPushButton, 2, 0, 1, 1)
        self.removeSelectedPushButton = QtGui.QPushButton(Dialog)
        self.removeSelectedPushButton.setObjectName(_fromUtf8("removeSelectedPushButton"))
        self.gridLayout_2.addWidget(self.removeSelectedPushButton, 2, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(642, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 2, 2, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.importPushButton = QtGui.QPushButton(Dialog)
        self.importPushButton.setObjectName(_fromUtf8("importPushButton"))
        self.horizontalLayout.addWidget(self.importPushButton)
        self.exportPushButton = QtGui.QPushButton(Dialog)
        self.exportPushButton.setObjectName(_fromUtf8("exportPushButton"))
        self.horizontalLayout.addWidget(self.exportPushButton)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 0, 1, 3)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QObject.connect(self.removeSelectedPushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.removeSelectedRows)
        QtCore.QObject.connect(self.newConstraintPushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.insertNewRow)
        QtCore.QObject.connect(self.importPushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.importConfiguration)
        QtCore.QObject.connect(self.exportPushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.exportConfiguration)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Constraint Checker Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.postgisConnectionLabel.setText(QtGui.QApplication.translate("Dialog", "PostGIS Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.newConstraintPushButton.setText(QtGui.QApplication.translate("Dialog", "New Constraint", None, QtGui.QApplication.UnicodeUTF8))
        self.removeSelectedPushButton.setText(QtGui.QApplication.translate("Dialog", "Remove Selected", None, QtGui.QApplication.UnicodeUTF8))
        self.importPushButton.setText(QtGui.QApplication.translate("Dialog", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.exportPushButton.setText(QtGui.QApplication.translate("Dialog", "Export", None, QtGui.QApplication.UnicodeUTF8))

