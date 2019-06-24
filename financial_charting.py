from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from pandas.plotting import register_matplotlib_converters
from UI_MainWindow import Ui_MainWindow
from QStockSearch import QStockSearch
import qdarkgraystyle
import sys

register_matplotlib_converters()

api_key = 'NXI8RVGAPCK335JL'


class MainChartWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.toolbar = self.addToolBar('SymbolSearch')
        self.toolbar.setMovable(False)
        self.search_bar = QStockSearch()
        self.search_bar.combo_search.lineEdit().setPlaceholderText('Search stock/currency symbols')
        self.toolbar.addWidget(self.search_bar)
        self.connect_signals()
        self.showMaximized()

    def connect_signals(self):
        self.search_bar.plot_data.connect(self.ui.workspace_tabs.plot_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    ex = MainChartWindow()
    sys.exit(app.exec_())

