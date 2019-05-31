import sys
import datetime
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, \
    QApplication, QDesktopWidget, qApp
from PyQt5.QtGui import QIcon
import qdarkgraystyle
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiArea, QMdiSubWindow, QTextEdit
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavToolBar
from matplotlib.dates import (MONDAY, DateFormatter,
                              WeekdayLocator, date2num)
from matplotlib.widgets import Cursor
from mpl_finance import plot_day_summary_ohlc

api_key = 'NXI8RVGAPCK335JL'


class MainChartWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        table_widget = WorkspaceTabs(self)
        self.setCentralWidget(table_widget)

        menubar = self.menuBar()

#                               #
#           FILE MENU           #
#                               #
        file_menu = menubar.addMenu('&File')

        new_menu = QMenu('New', self)
        new_space_act = QAction('Workspace', self)
        new_space_act.triggered.connect(table_widget.new_workspace)
        new_chart_act = QAction('Chart', self)
        new_chart_act.triggered.connect(table_widget.new_chart)
        new_menu.addAction(new_space_act)
        new_menu.addAction(new_chart_act)

        save_act = QAction('Save', self)

        save_all_act = QAction(QIcon('save.png'), '&Save All', self)
        save_all_act.setShortcut('Ctrl+S')

        open_act = QAction(QIcon('open.png'), '&Open', self)

        exit_act = QAction('&Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(qApp.quit)

        file_menu.addMenu(new_menu)
        file_menu.addAction(save_act)
        file_menu.addAction(save_all_act)
        file_menu.addAction(open_act)
        file_menu.addSeparator()
        file_menu.addAction(exit_act)

#                               #
#           EDIT MENU           #
#                               #
        edit_menu = menubar.addMenu('&Edit')

        undo_act = QAction(QIcon('undo.png'), 'Undo', self)
        redo_act = QAction(QIcon('redo.png'), 'Redo', self)
        cut_act = QAction(QIcon('cut.png'), '&Cut', self)
        copy_act = QAction(QIcon('copy.png'), '&Copy', self)
        paste_act = QAction(QIcon('paste.png'), '&Paste', self)

        edit_menu.addAction(undo_act)
        edit_menu.addAction(redo_act)
        edit_menu.addSeparator()
        edit_menu.addAction(cut_act)
        edit_menu.addAction(copy_act)
        edit_menu.addAction(paste_act)
        edit_menu.addAction(paste_act)

        screen = app.primaryScreen()
        size = screen.availableGeometry()

        s_rat = size.height()/size.width()

        s_unit = s_rat * size.height()*0.25

        self.resize(size.width()-s_unit, size.height()-s_unit)
        self.center()
        self.setWindowTitle('Financial Charting')
        self.showMaximized()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class WorkspaceTabs(QWidget):
    layout = None
    tabs = None
    mdi = []

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.resize(300, 200)
        self.tabs.setTabsClosable(True)
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def new_workspace(self):
        self.tabs.resize(300, 200)

        new_tab = QWidget()
        new_tab.layout = QVBoxLayout(new_tab)

        new_mdi = QMdiArea()
        self.mdi.append(new_mdi)

        new_tab.layout.addWidget(new_mdi)

        self.tabs.addTab(new_tab, "New Workspace")

    def new_chart(self):
        if self.tabs.count() > 0:
            # create new mdi sub window
            sub = QMdiSubWindow()
            sub.setWidget(Chart(self))
            sub.setWindowTitle("New Chart")
            self.mdi[self.tabs.currentIndex()].addSubWindow(sub)
            sub.show()
        else:
            self.new_workspace()
            self.new_chart()


class Chart(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        qfigWidget = QWidget()

        ts = TimeSeries(key=api_key, output_format='pandas')
#       data, meta_data = ts.get_intraday(symbol='MSFT', interval='1min', outputsize='full')

        forex = ForeignExchange(key=api_key, output_format='pandas')
        #fx_data, fx_meta_data = forex.get_currency_exchange_intraday(from_symbol='USD', to_symbol='CAD',
        #                                                      interval='1min')

        fx_data, fx_meta_data  = forex.get_currency_exchange_daily(from_symbol='USD', to_symbol='CAD',
                                                                   outputsize='compact')

        fx_data.index = pd.to_datetime(fx_data.index)

        # fig = Figure((5.0, 4.0), dpi=100)
        fig = plt.figure(figsize=(8, 6))
        axes = fig.add_subplot(111)

        canvas = FigureCanvas(fig)
        canvas.setParent(qfigWidget)
        toolbar = NavToolBar(canvas, qfigWidget)
        # axes = fig.add_subplot(111)
        # Tell matplotlib to interpret the x-axis values as dates
        axes.xaxis_date()
        axes.plot(fx_data['4. close'])
        axes.grid()

        # Make space for and rotate the x-axis tick labels
        fig.autofmt_xdate()
        cursor = Cursor(axes, useblit=True, color='gray', linewidth=1)

        def onclick(event):
            cursor.onmove(event)
        canvas.mpl_connect('button_press_event', onclick)
        canvas.draw()

        # place plot components in a layout
        plotLayout = QVBoxLayout()
        plotLayout.addWidget(canvas)
        plotLayout.addWidget(toolbar)
        qfigWidget.setLayout(plotLayout)

        # prevent the canvas to shrink beyond a point
        # original size looks like a good minimum size
        canvas.setMinimumSize(canvas.size())

        self.setLayout(plotLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    ex = MainChartWindow()
    sys.exit(app.exec_())

