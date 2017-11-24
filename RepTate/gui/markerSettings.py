# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/markerSettings.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(306, 420)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/Images/new_icons/icons8-color-wheel-2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.cbSymbolType = QtWidgets.QComboBox(self.groupBox_3)
        self.cbSymbolType.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cbSymbolType.setFont(font)
        self.cbSymbolType.setObjectName("cbSymbolType")
        self.verticalLayout_2.addWidget(self.cbSymbolType)
        self.rbFixedSymbol = QtWidgets.QRadioButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rbFixedSymbol.setFont(font)
        self.rbFixedSymbol.setChecked(True)
        self.rbFixedSymbol.setObjectName("rbFixedSymbol")
        self.verticalLayout_2.addWidget(self.rbFixedSymbol)
        self.rbVariableSymbol = QtWidgets.QRadioButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rbVariableSymbol.setFont(font)
        self.rbVariableSymbol.setChecked(False)
        self.rbVariableSymbol.setObjectName("rbVariableSymbol")
        self.verticalLayout_2.addWidget(self.rbVariableSymbol)
        self.spinBoxLineW = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.spinBoxLineW.setFont(font)
        self.spinBoxLineW.setDecimals(1)
        self.spinBoxLineW.setMinimum(0.1)
        self.spinBoxLineW.setMaximum(10.0)
        self.spinBoxLineW.setSingleStep(0.1)
        self.spinBoxLineW.setProperty("value", 1.0)
        self.spinBoxLineW.setObjectName("spinBoxLineW")
        self.verticalLayout_2.addWidget(self.spinBoxLineW)
        self.horizontalLayout.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.spinBox = QtWidgets.QSpinBox(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.spinBox.setFont(font)
        self.spinBox.setMaximum(40)
        self.spinBox.setSingleStep(3)
        self.spinBox.setProperty("value", 12)
        self.spinBox.setObjectName("spinBox")
        self.verticalLayout_3.addWidget(self.spinBox)
        self.rbEmpty = QtWidgets.QRadioButton(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rbEmpty.setFont(font)
        self.rbEmpty.setChecked(True)
        self.rbEmpty.setObjectName("rbEmpty")
        self.verticalLayout_3.addWidget(self.rbEmpty)
        self.rbFilled = QtWidgets.QRadioButton(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rbFilled.setFont(font)
        self.rbFilled.setObjectName("rbFilled")
        self.verticalLayout_3.addWidget(self.rbFilled)
        self.horizontalLayout.addWidget(self.groupBox_4)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.rbFixedColor = QtWidgets.QRadioButton(self.groupBox_5)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rbFixedColor.setFont(font)
        self.rbFixedColor.setObjectName("rbFixedColor")
        self.verticalLayout_5.addWidget(self.rbFixedColor)
        self.rbGradientColor = QtWidgets.QRadioButton(self.groupBox_5)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rbGradientColor.setFont(font)
        self.rbGradientColor.setObjectName("rbGradientColor")
        self.verticalLayout_5.addWidget(self.rbGradientColor)
        self.rbPalette = QtWidgets.QRadioButton(self.groupBox_5)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rbPalette.setFont(font)
        self.rbPalette.setChecked(True)
        self.rbPalette.setObjectName("rbPalette")
        self.verticalLayout_5.addWidget(self.rbPalette)
        self.horizontalLayout_3.addWidget(self.groupBox_5)
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.groupBox_6)
        self.label_4.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.labelPickedColor1 = QtWidgets.QLabel(self.groupBox_6)
        self.labelPickedColor1.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelPickedColor1.setFont(font)
        self.labelPickedColor1.setText("")
        self.labelPickedColor1.setObjectName("labelPickedColor1")
        self.gridLayout.addWidget(self.labelPickedColor1, 0, 1, 1, 1)
        self.pickColor1 = QtWidgets.QToolButton(self.groupBox_6)
        self.pickColor1.setEnabled(False)
        self.pickColor1.setObjectName("pickColor1")
        self.gridLayout.addWidget(self.pickColor1, 0, 2, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox_6)
        self.label_5.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.labelPickedColor2 = QtWidgets.QLabel(self.groupBox_6)
        self.labelPickedColor2.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelPickedColor2.setFont(font)
        self.labelPickedColor2.setText("")
        self.labelPickedColor2.setObjectName("labelPickedColor2")
        self.horizontalLayout_4.addWidget(self.labelPickedColor2)
        self.pickColor2 = QtWidgets.QToolButton(self.groupBox_6)
        self.pickColor2.setEnabled(False)
        self.pickColor2.setObjectName("pickColor2")
        self.horizontalLayout_4.addWidget(self.pickColor2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.cbPalette = QtWidgets.QComboBox(self.groupBox_6)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cbPalette.setFont(font)
        self.cbPalette.setObjectName("cbPalette")
        self.verticalLayout_4.addWidget(self.cbPalette)
        self.horizontalLayout_3.addWidget(self.groupBox_6)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushApply = QtWidgets.QPushButton(Dialog)
        self.pushApply.setObjectName("pushApply")
        self.horizontalLayout_5.addWidget(self.pushApply)
        self.pushCancel = QtWidgets.QPushButton(Dialog)
        self.pushCancel.setObjectName("pushCancel")
        self.horizontalLayout_5.addWidget(self.pushCancel)
        self.pushOK = QtWidgets.QPushButton(Dialog)
        self.pushOK.setObjectName("pushOK")
        self.horizontalLayout_5.addWidget(self.pushOK)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Dialog)
        self.rbFixedColor.clicked['bool'].connect(self.pickColor2.setDisabled)
        self.rbFixedColor.clicked['bool'].connect(self.cbPalette.setDisabled)
        self.rbGradientColor.clicked['bool'].connect(self.cbPalette.setDisabled)
        self.rbPalette.clicked['bool'].connect(self.pickColor1.setDisabled)
        self.rbPalette.clicked['bool'].connect(self.pickColor2.setDisabled)
        self.rbFixedSymbol.clicked['bool'].connect(self.cbSymbolType.setEnabled)
        self.rbPalette.clicked['bool'].connect(self.cbPalette.setEnabled)
        self.rbGradientColor.clicked['bool'].connect(self.pickColor1.setEnabled)
        self.rbGradientColor.clicked['bool'].connect(self.pickColor2.setEnabled)
        self.rbFixedColor.clicked['bool'].connect(self.pickColor1.setEnabled)
        self.pushOK.clicked.connect(Dialog.accept)
        self.pushCancel.clicked.connect(Dialog.reject)
        self.rbVariableSymbol.clicked['bool'].connect(self.cbSymbolType.setDisabled)
        self.rbPalette.clicked['bool'].connect(self.label_4.setDisabled)
        self.rbPalette.clicked['bool'].connect(self.label_5.setDisabled)
        self.rbGradientColor.clicked['bool'].connect(self.label_4.setEnabled)
        self.rbGradientColor.clicked['bool'].connect(self.label_5.setEnabled)
        self.rbFixedColor.clicked['bool'].connect(self.label_5.setDisabled)
        self.rbFixedColor.clicked['bool'].connect(self.label_4.setEnabled)
        self.rbPalette.clicked['bool'].connect(self.labelPickedColor1.setDisabled)
        self.rbPalette.clicked['bool'].connect(self.labelPickedColor2.setDisabled)
        self.rbGradientColor.clicked['bool'].connect(self.labelPickedColor1.setEnabled)
        self.rbGradientColor.clicked['bool'].connect(self.labelPickedColor2.setEnabled)
        self.rbFixedColor.clicked['bool'].connect(self.labelPickedColor2.setDisabled)
        self.rbFixedColor.clicked['bool'].connect(self.labelPickedColor1.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dataset Style"))
        self.groupBox.setTitle(_translate("Dialog", "Symbol"))
        self.groupBox_3.setTitle(_translate("Dialog", "Type"))
        self.rbFixedSymbol.setText(_translate("Dialog", "Fixed"))
        self.rbVariableSymbol.setText(_translate("Dialog", "Variable"))
        self.spinBoxLineW.setPrefix(_translate("Dialog", "Line width: "))
        self.groupBox_4.setTitle(_translate("Dialog", "Size"))
        self.rbEmpty.setText(_translate("Dialog", "Empty"))
        self.rbFilled.setText(_translate("Dialog", "Filled"))
        self.groupBox_2.setTitle(_translate("Dialog", "Color"))
        self.groupBox_5.setTitle(_translate("Dialog", "Type"))
        self.rbFixedColor.setText(_translate("Dialog", "Fixed"))
        self.rbGradientColor.setText(_translate("Dialog", "Gradient"))
        self.rbPalette.setText(_translate("Dialog", "Palette"))
        self.groupBox_6.setTitle(_translate("Dialog", "Selection"))
        self.label_4.setText(_translate("Dialog", "Color 1"))
        self.pickColor1.setText(_translate("Dialog", "..."))
        self.label_5.setText(_translate("Dialog", "Color 2"))
        self.pickColor2.setText(_translate("Dialog", "..."))
        self.pushApply.setText(_translate("Dialog", "Apply"))
        self.pushCancel.setText(_translate("Dialog", "Cancel"))
        self.pushOK.setText(_translate("Dialog", "OK"))

import Reptate_rc
