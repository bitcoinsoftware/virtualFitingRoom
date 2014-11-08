# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/gimbo/Desktop/koniu/src/guiFor_Wctt.ui'
#
# Created: Fri May 31 12:29:38 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from Connections import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object,  Connections):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(851, 641)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.pushButton = QtGui.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(350, 90, 151, 21))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(520, 90, 161, 21))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.centralWidget)
        self.pushButton_3.setGeometry(QtCore.QRect(690, 60, 151, 21))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.kurlcomborequester = KUrlComboRequester(self.centralWidget)
        self.kurlcomborequester.setGeometry(QtCore.QRect(20, 30, 321, 27))
        self.kurlcomborequester.setObjectName(_fromUtf8("kurlcomborequester"))
        self.kurlcomborequester_2 = KUrlComboRequester(self.centralWidget)
        self.kurlcomborequester_2.setGeometry(QtCore.QRect(350, 30, 281, 27))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.kurlcomborequester_2.setFont(font)
        self.kurlcomborequester_2.setObjectName(_fromUtf8("kurlcomborequester_2"))
        self.kurlcomborequester_3 = KUrlComboRequester(self.centralWidget)
        self.kurlcomborequester_3.setGeometry(QtCore.QRect(20, 80, 321, 27))
        self.kurlcomborequester_3.setObjectName(_fromUtf8("kurlcomborequester_3"))
        self.label = QtGui.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 201, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(350, 10, 111, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(20, 60, 111, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.pushButton_4 = QtGui.QPushButton(self.centralWidget)
        self.pushButton_4.setGeometry(QtCore.QRect(520, 60, 161, 21))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.graphicsView = QtGui.QGraphicsView(self.centralWidget)
        self.graphicsView.setGeometry(QtCore.QRect(20, 140, 191, 301))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.graphicsView_2 = QtGui.QGraphicsView(self.centralWidget)
        self.graphicsView_2.setGeometry(QtCore.QRect(240, 140, 281, 491))
        self.graphicsView_2.setObjectName(_fromUtf8("graphicsView_2"))
        self.graphicsView_3 = QtGui.QGraphicsView(self.centralWidget)
        self.graphicsView_3.setGeometry(QtCore.QRect(550, 140, 291, 491))
        self.graphicsView_3.setObjectName(_fromUtf8("graphicsView_3"))
        self.pushButton_5 = QtGui.QPushButton(self.centralWidget)
        self.pushButton_5.setGeometry(QtCore.QRect(350, 60, 151, 21))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.graphicsView_4 = QtGui.QGraphicsView(self.centralWidget)
        self.graphicsView_4.setGeometry(QtCore.QRect(20, 450, 191, 181))
        self.graphicsView_4.setObjectName(_fromUtf8("graphicsView_4"))
        self.label_4 = QtGui.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(640, 10, 191, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.kurlcomborequester_4 = KUrlComboRequester(self.centralWidget)
        self.kurlcomborequester_4.setGeometry(QtCore.QRect(640, 30, 201, 27))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.kurlcomborequester_4.setFont(font)
        self.kurlcomborequester_4.setObjectName(_fromUtf8("kurlcomborequester_4"))
        MainWindow.setCentralWidget(self.centralWidget)
        self.connect()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "2.Wyodrebnij kontury", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "4.Rozpoznaj czesci ciala", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("MainWindow", "5.Przymierz ubranie", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Zdjecie osoby", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Zdjecie tla", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Zdjecie ubrania", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("MainWindow", "3.Wyodrebnij cialo", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("MainWindow", "1.Wyswietl argumenty", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Prepared body points", None, QtGui.QApplication.UnicodeUTF8))

from PyKDE4.kio import KUrlComboRequester

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

