from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from pandas.plotting import register_matplotlib_converters
from UI_MainWindow import Ui_MainWindow
from QComboSearch import QComboSearch
import qdarkgraystyle
import sys
import csv

register_matplotlib_converters()

api_key = 'NXI8RVGAPCK335JL'


class MainChartWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        toolbar = self.addToolBar('SymbolSearch')
        toolbar.setMovable(False)
        search_bar = SymbolSearch()
        toolbar.addWidget(search_bar)
        self.showMaximized()


class SymbolSearch(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()

        # search bar to find stocks, or physical/digital currency symbols
        self.combo_search = QComboSearch()
        self.combo_search.setMaximumWidth(800)
        self.combo_search.setCurrentText('Search for a symbol or currency')
        self.combo_search.setToolTip("Type here to find stock, or a physical/digital currency symbols")

        # button to add the selected symbols to the current chart
        self.btn_add = QPushButton(self)
        self.btn_add.setMaximumSize(QSize(100, 16777215))
        self.btn_add.setObjectName("btn_add")
        self.btn_add.setToolTip("<html><head/><body><p>Chart the selected symbol, or add to the current chart</p></body></html>")
        self.btn_add.setText("Add")

        self.layout.addWidget(self.combo_search)
        self.layout.addWidget(self.btn_add)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setMinimumWidth(600)
        self.setLayout(self.layout)

    # def make_currency_list(self, fileName):
        # TODO: also compile a list of all available digital currencies paired with
        #       each currency market eg BTC/CAD

        # 1. make a dictionary for all single currencies, assigning the key as
        #    an incremented number(eg 1-633). The data will consist of an
        #    enumeration and 2 strings. The enumeration will identify what type
        #    of currency(physical or digital) and a string for the symbol (eg CAD)
        #    and another string for metadata (eg Canadian Dollar)
        # 2. compile a third dictionary for every possible currency pair.
        #    Assign each key as the concatenation of the two currencies in the pair
        #    (eg CAD=121, USD=023, USDCAD=023121) this gives access to the dictionary
        #    with data(enumeration, symbol, metadata)


        # 1. cylce csv list of currencies
        # 2. for each currency(first 4 chars that are not ' ' on each row)
        #    concatenate currency with every other currency excluding itself
        # 3. add each pair to a list which will be the elements of the combobox
        # cur_list = []
        # data_list = []
        # with open('physical_currency_list.csv', "r") as fileInput:
        #     reader = csv.reader(fileInput)
        #     next(reader, None)
        #     for row in reader:
        #         items = [
        #             str(field)
        #             for field in row
        #         ]
        #
        #         cur_list.append(items[0])
        #         data_list.append(items[1])
        #
        # with open('digital_currency_list.csv', "r") as fileInput:
        #     reader = csv.reader(fileInput)
        #     next(reader, None)
        #     for row in reader:
        #         items = [
        #             str(field)
        #             for field in row
        #         ]
        #
        #         cur_list.append(items[0])
        #         data_list.append(items[1])

        # currency_pairs = []
        # for i1, val1 in enumerate(cur_list):
        #     for i2, val2 in enumerate(cur_list):
        #         if val1 != val2:
        #             currency_pairs.append(val1 + val2 +
        #                                   "\t" + data_list[i1] + " \\ " + data_list[i2])
        # return currency_pairs


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    ex = MainChartWindow()
    sys.exit(app.exec_())

