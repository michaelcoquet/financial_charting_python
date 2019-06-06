#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5 import QtCore
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QCompleter, QComboBox
import csv

class QComboSearch(QComboBox):
    def __init__(self, parent=None):
        super(QComboSearch, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)

        # check if line edit has ever been changed
        self.textChanged = False

    # on selection of an item from the completer, select the corresponding item from combobox 
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))

    # on model change, update the models of the filter and completer as well 
    def setModel(self, model):
        super(QComboSearch, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(QComboSearch, self).setModelColumn(column)

    def keyPressEvent(self, event):
        if (type(event) == QKeyEvent) and (self.textChanged == False):
            self.setCurrentText("")
            self.textChanged = True
        super(QComboSearch, self).keyPressEvent(event)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QStringListModel

    app = QApplication(sys.argv)

    with open('physical_currency_list.csv', "r") as fileInput:
        reader = csv.reader(fileInput)
        next(reader, None)
        string_list = []
        for row in reader:
            items = [
                str(field)
                for field in row
            ]

            cur = items[0] + "\t" + items[1]
            string_list.append(cur)

    combo = QComboSearch()
    # either fill the standard model of the combobox
    combo.addItems(string_list)
    combo.setCurrentText("this is default")

    # or use another model
    #combo.setModel(QStringListModel(string_list))

    combo.resize(300, 40)
    combo.show()

    sys.exit(app.exec_())