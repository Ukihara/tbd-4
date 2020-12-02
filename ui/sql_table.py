from typing import Any, List
from PySide2.QtCore import QModelIndex
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem
from collections import namedtuple


SelectedItemInfo = namedtuple("SelectedItemInfo", ["row_index", "column_index", "value"])

class SQLTableWidget():
    '''
        wrapper to add functionality to default QTableWidget
    '''

    def __init__(self, qtable : QTableWidget, id_column_index : int = 0):
        self.wrapped_table = qtable
        self.id_column_index = id_column_index

    def __getattr__(self, name: str) -> Any:
        if name in self.wrapped_table.__dict__:
            return self.wrapped_table.__getattribute__(name)
        elif name in self.__dict__:
            return self.__dict__[name]
        else:
            raise AttributeError

    def show_query_resluts(self, header : list, rows : list) -> None:
        self.wrapped_table.setColumnCount(len(header))
        self.wrapped_table.setRowCount(len(rows))

        for i, c_name in enumerate(header):
            self.wrapped_table.setHorizontalHeaderItem(i, QTableWidgetItem(c_name))

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.wrapped_table.setItem(i, j, QTableWidgetItem(str(value)))

    def get_selected_items(self) -> List[SelectedItemInfo]:
        selected_items = [SelectedItemInfo(x.row(), x.column(), x.data()) for x in self.wrapped_table.selectedIndexes()]
        return selected_items

    def delete_rows(self, rows_indexes : List[int]):
        for i, index in enumerate(sorted(rows_indexes)):
            self.wrapped_table.removeRow(index - i)

    def get_sqlid(self, row_id : int) -> str:
        return self.wrapped_table.item(row_id, self.id_column_index).text()

    def get_sqlid_column_name(self) -> str:
        return self.wrapped_table.horizontalHeaderItem(self.id_column_index).text()

    def get_column_name(self, c_index : int) -> str:
        return self.wrapped_table.horizontalHeaderItem(c_index).text()

    # def append_row(self) -> None:
    #     self.wrapped_table.insertRow(0)
        
        