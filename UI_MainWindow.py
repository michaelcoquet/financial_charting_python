# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(10, 2, 10, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.workspace_tabs = WorkspaceTabs(self.centralwidget)
        self.workspace_tabs.setObjectName("workspace_tabs")
        self.horizontalLayout.addWidget(self.workspace_tabs)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 44))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_New = QtWidgets.QMenu(self.menu_File)
        self.menu_New.setObjectName("menu_New")
        self.menu_Edit = QtWidgets.QMenu(self.menubar)
        self.menu_Edit.setObjectName("menu_Edit")
        self.menu_Add = QtWidgets.QMenu(self.menubar)
        self.menu_Add.setObjectName("menu_Add")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setMovable(False)
        self.toolBar.setAllowedAreas(QtCore.Qt.TopToolBarArea)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_Open = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Open.setIcon(icon)
        self.action_Open.setObjectName("action_Open")
        self.action_Save = QtWidgets.QAction(MainWindow)
        self.action_Save.setObjectName("action_Save")
        self.action_Save_All = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Save_All.setIcon(icon1)
        self.action_Save_All.setObjectName("action_Save_All")
        self.action_Exit = QtWidgets.QAction(MainWindow)
        self.action_Exit.setObjectName("action_Exit")
        self.action_Undo = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/undo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Undo.setIcon(icon2)
        self.action_Undo.setObjectName("action_Undo")
        self.action_Redo = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/redo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Redo.setIcon(icon3)
        self.action_Redo.setObjectName("action_Redo")
        self.action_Cut = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/cut.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Cut.setIcon(icon4)
        self.action_Cut.setObjectName("action_Cut")
        self.action_Copy = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Copy.setIcon(icon5)
        self.action_Copy.setObjectName("action_Copy")
        self.action_Paste = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/paste.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Paste.setIcon(icon6)
        self.action_Paste.setObjectName("action_Paste")
        self.action_Indicator = QtWidgets.QAction(MainWindow)
        self.action_Indicator.setObjectName("action_Indicator")
        self.action_Workspace = QtWidgets.QAction(MainWindow)
        self.action_Workspace.setObjectName("action_Workspace")
        self.action_Chart = QtWidgets.QAction(MainWindow)
        self.action_Chart.setObjectName("action_Chart")
        self.menu_New.addAction(self.action_Workspace)
        self.menu_New.addAction(self.action_Chart)
        self.menu_File.addAction(self.menu_New.menuAction())
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addAction(self.action_Save_All)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Exit)
        self.menu_Edit.addAction(self.action_Undo)
        self.menu_Edit.addAction(self.action_Redo)
        self.menu_Edit.addSeparator()
        self.menu_Edit.addAction(self.action_Cut)
        self.menu_Edit.addAction(self.action_Copy)
        self.menu_Edit.addAction(self.action_Paste)
        self.menu_Add.addAction(self.action_Indicator)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_Add.menuAction())

        self.retranslateUi(MainWindow)
        self.action_Exit.triggered.connect(MainWindow.close)
        self.action_Chart.triggered.connect(self.workspace_tabs.new_chart)
        self.action_Workspace.triggered.connect(self.workspace_tabs.new_workspace)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_New.setTitle(_translate("MainWindow", "&New"))
        self.menu_Edit.setTitle(_translate("MainWindow", "&Edit"))
        self.menu_Add.setTitle(_translate("MainWindow", "&Add"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_Open.setText(_translate("MainWindow", "&Open"))
        self.action_Save.setText(_translate("MainWindow", "&Save"))
        self.action_Save.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.action_Save_All.setText(_translate("MainWindow", "Save &All"))
        self.action_Save_All.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.action_Exit.setText(_translate("MainWindow", "&Exit"))
        self.action_Exit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.action_Undo.setText(_translate("MainWindow", "&Undo"))
        self.action_Undo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.action_Redo.setText(_translate("MainWindow", "&Redo"))
        self.action_Redo.setShortcut(_translate("MainWindow", "Ctrl+Y"))
        self.action_Cut.setText(_translate("MainWindow", "Cu&t"))
        self.action_Cut.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.action_Copy.setText(_translate("MainWindow", "&Copy"))
        self.action_Copy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.action_Paste.setText(_translate("MainWindow", "&Paste"))
        self.action_Paste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.action_Indicator.setText(_translate("MainWindow", "&Indicator"))
        self.action_Workspace.setText(_translate("MainWindow", "&Workspace"))
        self.action_Chart.setText(_translate("MainWindow", "&Chart"))
        self.action_Chart.setShortcut(_translate("MainWindow", "Ctrl+N"))


from WorkspaceTabs import WorkspaceTabs
# import resources_rc
