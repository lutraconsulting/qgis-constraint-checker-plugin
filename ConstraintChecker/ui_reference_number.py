# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_reference_number.ui'
#
# Created: Mon Mar 24 09:50:13 2014
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
        Dialog.resize(253, 67)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.referenceNumberLabel = QtGui.QLabel(Dialog)
        self.referenceNumberLabel.setObjectName(_fromUtf8("referenceNumberLabel"))
        self.gridLayout.addWidget(self.referenceNumberLabel, 0, 0, 1, 1)
        self.referenceNumberLineEdit = QtGui.QLineEdit(Dialog)
        self.referenceNumberLineEdit.setObjectName(_fromUtf8("referenceNumberLineEdit"))
        self.gridLayout.addWidget(self.referenceNumberLineEdit, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Reference Number", None, QtGui.QApplication.UnicodeUTF8))
        self.referenceNumberLabel.setText(QtGui.QApplication.translate("Dialog", "Reference Number", None, QtGui.QApplication.UnicodeUTF8))

