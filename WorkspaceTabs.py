from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMdiArea, QMdiSubWindow, QTabWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavToolBar
from matplotlib.widgets import Cursor
import matplotlib.pyplot as plt


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
        #qfigWidget = QWidget()

        #ts = TimeSeries(key=api_key, output_format='pandas')
#       data, meta_data = ts.get_intraday(symbol='MSFT', interval='1min', outputsize='full')

        #forex = ForeignExchange(key=api_key, output_format='pandas')
        #fx_data, fx_meta_data = forex.get_currency_exchange_intraday(from_symbol='USD', to_symbol='CAD',
        #                                                      interval='1min')

        #fx_data, fx_meta_data  = forex.get_currency_exchange_daily(from_symbol='USD', to_symbol='CAD',
        #                                                           outputsize='compact')

        #fx_data.index = pd.to_datetime(fx_data.index)

        # fig = Figure((5.0, 4.0), dpi=100)
        fig = plt.figure(figsize=(8, 6))
        axes = fig.add_subplot(111)

        canvas = FigureCanvas(fig)
        canvas.setParent(self)
        toolbar = NavToolBar(canvas, self)
        # axes = fig.add_subplot(111)
        # Tell matplotlib to interpret the x-axis values as dates
        axes.xaxis_date()
        #plot_day_summary_ohlc(axes, zip(date2num(fx_data.index), fx_data['1. open'], fx_data['2. high'],
        #                              fx_data['3. low'], fx_data['4. close']))
        #axes.plot(fx_data['4. close'])
        axes.grid()

        # Make space for and rotate the x-axis tick labels
        fig.autofmt_xdate()
        cursor = Cursor(axes, useblit=True, color='gray', linewidth=1)

        def onclick(event):
            cursor.onmove(event)
        canvas.mpl_connect('button_press_event', onclick)
        canvas.draw()

        # place plot components in a layout
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(canvas)
        plot_layout.addWidget(toolbar)
        self.setLayout(plot_layout)

        # prevent the canvas to shrink beyond a point
        # original size looks like a good minimum size
        canvas.setMinimumSize(canvas.size())

        self.setLayout(plot_layout)