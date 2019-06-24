from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMdiArea, QMdiSubWindow, QTabWidget
from PyQt5.QtCore import pyqtSlot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavToolBar
from matplotlib.widgets import Cursor
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from matplotlib.figure import Figure
from mpl_finance import plot_day_summary_ohlc
from pandas import to_datetime
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
from alpha_vantage.cryptocurrencies import CryptoCurrencies
api_key = 'NXI8RVGAPCK335JL'


class WorkspaceTabs(QTabWidget):
    mdi = []

    def __init__(self, parent):
        super().__init__(parent)
        #self.layout = QVBoxLayout(self)
        # # Initialize tab screen
        self.resize(300, 200)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setMinimumHeight(100)

    @pyqtSlot(list)
    def plot_data(self, data):
        if self.count() == 0:
            # no tabs are currently open so open a new workspace and chart
            # for the new data
            self.new_workspace()
            self.new_chart()
            # plot the new data on the new chart
            self.mdi[self.currentIndex()].currentSubWindow().widget().plot_data(data)
        else:
            # since a tab is already open then plot the data on the active
            # subwindow
            print('not 00')

    def new_workspace(self):
        self.resize(300, 200)

        new_tab = QWidget()
        new_tab.layout = QVBoxLayout(new_tab)

        new_mdi = QMdiArea()
        self.mdi.append(new_mdi)

        new_tab.layout.addWidget(new_mdi)

        self.addTab(new_tab, "New Workspace")

    def new_chart(self):
        if self.count() > 0:
            # create new mdi sub window
            # TODO: create a new dialog that asks the user which instrument to chart
            #       and place that in the appropriate workspace tab
            sub = QMdiSubWindow()
            sub.setWidget(Chart(self))
            sub.setWindowTitle("New Chart")
            self.mdi[self.currentIndex()].addSubWindow(sub)
            sub.show()
        else:
            # TODO: create a new dialog that asks the user which instrument to chart
            #       and place that in the appropriate workspace tab
            self.new_workspace()
            self.new_chart()


class Chart(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        # # ts = TimeSeries(key=api_key, output_format='pandas')
        # #       data, meta_data = ts.get_intraday(symbol='MSFT', interval='1min', outputsize='full')
        # #
        # forex = ForeignExchange(key=api_key, output_format='pandas')
        # fx_data, fx_meta_data = forex.get_currency_exchange_intraday(from_symbol='USD', to_symbol='CAD',
        #                                                      interval='1min')
        # #
        # # fx_data, fx_meta_data = forex.get_currency_exchange_daily(from_symbol='USD', to_symbol='CAD',
        # #                                                           outputsize='compact')
        # #
        # fx_data.index = to_datetime(fx_data.index)
        #
        # fig = Figure((5.0, 4.0), dpi=100)
        self.fig = plt.figure(figsize=(8, 6))
        self.axes = self.fig.add_subplot(111)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.toolbar = NavToolBar(self.canvas, self)
        # axes = fig.add_subplot(111)
        # Tell matplotlib to interpret the x-axis values as dates
        self.axes.xaxis_date()
        # plot_day_summary_ohlc(self.axes, zip(date2num(fx_data.index), fx_data['1. open'], fx_data['2. high'],
        #                               fx_data['3. low'], fx_data['4. close']))
        self.axes.grid()

        # Make space for and rotate the x-axis tick labels
        self.fig.autofmt_xdate()
        self.cursor = Cursor(self.axes, useblit=True, color='gray', linewidth=1)

        def onclick(event):
            self.cursor.onmove(event)
        self.canvas.mpl_connect('button_press_event', onclick)
        self.canvas.draw()

        # place plot components in a layout
        self.plotLayout = QVBoxLayout()
        self.plotLayout.addWidget(self.canvas)
        self.plotLayout.addWidget(self.toolbar)
        self.setLayout(self.plotLayout)

        # prevent the canvas to shrink beyond a point
        # original size looks like a good minimum size
        self.canvas.setMinimumSize(self.canvas.size())

        self.setLayout(self.plotLayout)

    def plot_data(self, data):
        data = data[0]
        if data[0] == 'physical':
            forex = ForeignExchange(key=api_key, output_format='pandas')
            fx_data, fx_meta_data = forex.get_currency_exchange_daily(from_symbol=data[2], to_symbol=data[3],
                                                                      outputsize='compact')
            fx_data.index = to_datetime(fx_data.index)

            self.axes.set_ylim(min(fx_data['3. low']), max(fx_data['2. high']))
            self.axes.set_xlim(min(fx_data.index), max(fx_data.index))

            plot_day_summary_ohlc(self.axes, zip(date2num(fx_data.index), fx_data['1. open'], fx_data['2. high'],
                                                 fx_data['3. low'], fx_data['4. close']))
        elif data[0] == 'digital':
            cryptex = CryptoCurrencies(key=api_key, output_format='pandas')
            cx_data, cx_meta_data = cryptex.get_digital_currency_weekly(symbol=data[2], market=data[3])
            cx_data.index = to_datetime(cx_data.index)

            self.axes.set_ylim(min(cx_data['3a. low (' + data[3] + ')']),
                               max(cx_data['2a. high (' + data[3] + ')']))
            self.axes.set_xlim(min(cx_data.index), max(cx_data.index))

            plot_day_summary_ohlc(self.axes, zip(date2num(cx_data.index),
                                                 cx_data['1a. open (' + data[3] + ')'],
                                                 cx_data['2a. high (' + data[3] + ')'],
                                                 cx_data['3a. low (' + data[3] + ')'],
                                                 cx_data['4a. close (' + data[3] + ')']))
        elif data[0] == 'stock':
            # TODO: make this plot for any stock from searchbar, instaed of testing
            #       forex plotting
            forex = ForeignExchange(key=api_key, output_format='pandas')
            fx_data, fx_meta_data = forex.get_currency_exchange_intraday(from_symbol='USD', to_symbol='CAD',
                                                                         interval='1min')
            fx_data.index = to_datetime(fx_data.index)

            self.axes.set_ylim(min(fx_data['3. low']), max(fx_data['2. high']))
            self.axes.set_xlim(min(fx_data.index), max(fx_data.index))

            plot_day_summary_ohlc(self.axes, zip(date2num(fx_data.index), fx_data['1. open'], fx_data['2. high'],
                                                 fx_data['3. low'], fx_data['4. close']))
