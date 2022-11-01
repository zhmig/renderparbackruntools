# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tools.ui'
#
# Created: Mon Oct 31 20:46:23 2022
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(486, 439)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.main_layer = QtWidgets.QGridLayout()
        self.main_layer.setObjectName("main_layer")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.filepath_Lb = QtWidgets.QLabel(self.centralwidget)
        self.filepath_Lb.setObjectName("filepath_Lb")
        self.horizontalLayout.addWidget(self.filepath_Lb)
        self.filepath_Le = QtWidgets.QLineEdit(self.centralwidget)
        self.filepath_Le.setObjectName("filepath_Le")
        self.horizontalLayout.addWidget(self.filepath_Le)
        self.filepath_Btn = QtWidgets.QPushButton(self.centralwidget)
        self.filepath_Btn.setObjectName("filepath_Btn")
        self.horizontalLayout.addWidget(self.filepath_Btn)
        self.main_layer.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.main_layer, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 486, 26))
        self.menubar.setObjectName("menubar")
        self.proj_menu = QtWidgets.QMenu(self.menubar)
        self.proj_menu.setObjectName("proj_menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.proj_setting_menu = QtWidgets.QAction(MainWindow)
        self.proj_setting_menu.setObjectName("proj_setting_menu")
        self.actiondi = QtWidgets.QAction(MainWindow)
        self.actiondi.setCheckable(True)
        self.actiondi.setObjectName("actiondi")
        self.actiongao = QtWidgets.QAction(MainWindow)
        self.actiongao.setCheckable(True)
        self.actiongao.setObjectName("actiongao")
        self.updataMenu = QtWidgets.QAction(MainWindow)
        self.updataMenu.setObjectName("updataMenu")
        self.proj_menu.addAction(self.proj_setting_menu)
        self.proj_menu.addSeparator()
        self.proj_menu.addAction(self.updataMenu)
        self.proj_menu.addSeparator()
        self.menubar.addAction(self.proj_menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.filepath_Lb.setText(QtWidgets.QApplication.translate("MainWindow", "文件路径：", None, -1))
        self.filepath_Btn.setText(QtWidgets.QApplication.translate("MainWindow", "<<<", None, -1))
        self.proj_menu.setTitle(QtWidgets.QApplication.translate("MainWindow", "项目", None, -1))
        self.proj_setting_menu.setText(QtWidgets.QApplication.translate("MainWindow", "设置", None, -1))
        self.actiondi.setText(QtWidgets.QApplication.translate("MainWindow", "低质量", None, -1))
        self.actiongao.setText(QtWidgets.QApplication.translate("MainWindow", "高质量", None, -1))
        self.updataMenu.setText(QtWidgets.QApplication.translate("MainWindow", "刷新", None, -1))

