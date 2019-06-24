#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QWidget, QCompleter, QComboBox, QHBoxLayout, \
                            QPushButton, QLineEdit, QListView
import sqlite3
import os
import csv


class QStockSearch(QWidget):
    plot_data = pyqtSignal(list)

    def __init__(self, parent=None):
        super(QStockSearch, self).__init__(parent)
        self.layout = QHBoxLayout()

        # search bar to find stocks, or physical/digital currency symbols
        self.combo_search = ExtCombo()

        # button to add the selected symbols to the current chart
        self.btn_add = QPushButton(self)
        self.btn_add.setMaximumSize(QSize(100, 16777215))
        self.btn_add.setObjectName("btn_add")
        self.btn_add.setToolTip("<html><head/><body><p>Chart the selected symbol, or add to the current chart</p></body></html>")
        self.btn_add.setText("Add")
        self.btn_add.clicked.connect(self.emit_plot_signal)

        self.layout.addWidget(self.combo_search)
        self.layout.addWidget(self.btn_add)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setMinimumWidth(600)
        self.setLayout(self.layout)

    def emit_plot_signal(self):
        data = self.combo_search.get_list(self.combo_search.currentText())
        if data is not None:
            self.plot_data.emit(data)

    # function to help build the database of symbols
    # TODO: instead of downloading the lists manually make this function get it automatically
    #       from the website. Use this to periodically update the database to include newly
    #       added symbols
    @staticmethod
    def build_symbol_db(conn):
        cur = conn.cursor()
        total = 59554
        done = 0
        conn.execute('DELETE FROM stocks')
        for filename in os.listdir('./symbol_lists'):
            with open('./symbol_lists/' + filename , 'r') as f:
                filename = filename[:-4]
                reader = csv.reader(f, dialect='excel', delimiter='\t')
                next(reader, None)
                for row in reader:
                    done = done + 1
                    print("Progress: " + str((done / total) * 100))
                    try:
                        cur.execute("""INSERT INTO stocks VALUES (?, ?, ?, ?)""", (filename,
                                                                                   row[0],
                                                                                   row[1],
                                                                                   row[0] + "\t" + row[1]))
                        conn.commit()
                    except:
                        conn.rollback()


class ExtCombo(QComboBox):
    def __init__(self, parent=None):
        super(ExtCombo, self).__init__(parent)
        self.setMaximumWidth(800)
        self.setToolTip("Type here to find stock, or a physical/digital currency symbols")
        self.font = QFont()
        self.font.setFamily("Noto Mono")
        self.b_font = QFont()
        self.b_font.setFamily("Noto Mono")
        self.b_font.setBold(True)
        self.b_font.setUnderline(True)
        self.b_font.setPointSize(13)
        self.setFont(self.font)
        self.view().setFont(self.font)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.setMaxVisibleItems(20)
        self.setFocusPolicy(Qt.StrongFocus)
        # model used for combobox in search_db() function
        self.std_model = QStandardItemModel()

        # # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())
        #
        # # add a completer, which uses the filter model
        self.completer = QCompleter(self)
        self.completer.setMaxVisibleItems(20)
        # # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)
        # connect to the database of stock/currency symbols to search from
        self.database = "symbols.db"
        self.db_conn = sqlite3.connect(self.database)

        # perform this function whenever combobox text changes
        # self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.lineEdit().textEdited.connect(self.search_db)
        self.completer.activated.connect(self.on_completer_activated)
        self.keys_pressed = 0

    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, text):
        if text != "" and text != "Digital Currencies:":
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))

    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(ExtCombo, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    # search_db: searches the database of stock/currency symbols after each keypress
    #            and outputs the top 4 results from each type of symbol (physical cu
    #            rrency, digital currency, and stock) to the dropdown of the combobo
    #            x.
    def search_db(self):
        text = self.currentText()
        self.std_model.clear()
        phys_rows = self.select_text(text, "physical")
        dig_rows = self.select_text(text, "digital")
        stck_rows = self.select_text(text, "stocks")

        if len(stck_rows) != 0:
            header = QStandardItem("Stock Symbols:")
            header.setFont(self.b_font)
            self.std_model.appendRow(header)
            for row in stck_rows:
                items = QStandardItem(row)
                # items.setSelectable(True)
                self.std_model.appendRow(items)
            footer = QStandardItem("")
            # footer.setSelectable(False)
            self.std_model.appendRow(footer)

        if len(phys_rows) != 0:
            header = QStandardItem("Physical Currencies:")
            # header.setSelectable(False)
            header.setFont(self.b_font)
            self.std_model.appendRow(header)
            for row in phys_rows:
                items = QStandardItem(row)
                items.setSelectable(True)
                self.std_model.appendRow(items)
            footer = QStandardItem("")
            # footer.setSelectable(False)
            self.std_model.appendRow(footer)

        if len(dig_rows) != 0:
            header = QStandardItem("Digital Currencies:")
            # header.setSelectable(False)
            header.setFont(self.b_font)
            self.std_model.appendRow(header)
            for row in dig_rows:
                items = QStandardItem(row)
                items.setSelectable(True)
                self.std_model.appendRow(items)
            footer = QStandardItem("")
            # footer.setSelectable(False)
            self.std_model.appendRow(footer)

        self.setModel(self.std_model)
        self.setCurrentText(text)

    def get_list(self, metadata):
        cur = self.db_conn.cursor()

        cur.execute("SELECT * FROM stocks WHERE metadata like '" + metadata + "'")
        s = cur.fetchall()
        if s:
            return s
        cur.execute("SELECT * FROM physical_pairs WHERE metadata like '" + metadata + "'")
        p = cur.fetchall()
        if p:
            return p
        cur.execute("SELECT * FROM digital_pairs WHERE metadata like '" + metadata + "'")
        d = cur.fetchall()
        if d:
            return d

    # executes the sql command to find matches from the database
    def select_text(self, s, symbol_type):
        cur = self.db_conn.cursor()
        if symbol_type != 'stocks':
            cur.execute("SELECT metadata FROM " + symbol_type + "_pairs WHERE symbol like '%" + s + "%' LIMIT 4")
        else:
            cur.execute("SELECT metadata FROM " + symbol_type +
                        " WHERE symbol like '%" + s + "%' or "
                        "description like '%" + s + "%' LIMIT 4")

        items = cur.fetchall()

        rows = []
        for item in items:
            rows.append(item[0])

        return rows


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # database = "symbols.db"
    # db_conn = sqlite3.connect(database)
    # QStockSearch.build_symbol_db(db_conn)

    combo = QStockSearch()
    combo.combo_search.lineEdit().setPlaceholderText('dddd')
    combo.resize(1000, 40)
    combo.show()

    sys.exit(app.exec_())
