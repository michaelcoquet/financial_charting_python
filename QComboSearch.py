#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QCompleter, QComboBox
import sqlite3
from sqlite3 import Error


class QComboSearch(QComboBox):

    def __init__(self, parent=None):
        super(QComboSearch, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        font = QFont()
        font.setFamily("Noto Mono")
        self.setFont(font)
        self.view().setFont(font)
        self.setEditable(True)

        #self.load_data('')
        # # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        # self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        # self.pFilterModel.setSourceModel(self.model())
        #
        # # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # # always show all (filtered) completions
        # self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        # self.setCompleter(self.completer)
        #
        # # connect signals
        # self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)

        self.lineEdit().textEdited.connect(self.load_data)

        # check if line edit has ever been changed
        self.textChanged = False
        # self.data_loaded = False
    #
    # # on selection of an item from the completer, select the corresponding item from combobox

    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))

    #
    # # on model change, update the models of the filter and completer as well
    # def setModel(self, model):
    #     super(QComboSearch, self).setModel(model)
    #     self.pFilterModel.setSourceModel(model)
    #     self.completer.setModel(self.pFilterModel)
    #
    # # on model column change, update the model column of the filter and completer as well
    # def setModelColumn(self, column):
    #     self.completer.setCompletionColumn(column)
    #     self.pFilterModel.setFilterKeyColumn(column)
    #     super(QComboSearch, self).setModelColumn(column)

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if self.textChanged is False:
                self.setCurrentText("")
                self.textChanged = True
        super(QComboSearch, self).keyPressEvent(event)

    def load_data(self):
        database = "Currencies.db"
        conn = sqlite3.connect(database)
        text = self.currentText()
        phys_rows = self.select_text(conn, text, "physical")
        dig_rows = self.select_text(conn, text, "digital")
        self.clear()
        self.addItems(phys_rows)
        self.addItems(dig_rows)
        self.setCurrentText(text)

    def select_text(self, conn, s, type):
        cur = conn.cursor()
        cur.execute("SELECT metadata FROM " + type + "_pairs WHERE symbol like '%" + s + "%'")
        items = cur.fetchall()

        rows = []
        for item in items:
            rows.append(item[0])

        return rows


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QStringListModel

    app = QApplication(sys.argv)

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

    combo = QComboSearch()
    # either fill the standard model of the combobox
    #combo.addItems(currency_pairs)
    combo.setCurrentText("this is default")

    # or use another model
    #combo.setModel(QStringListModel(string_list))

    combo.resize(300, 40)
    combo.show()

    sys.exit(app.exec_())