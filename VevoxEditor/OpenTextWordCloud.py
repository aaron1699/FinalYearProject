import PyQt5.QtWidgets as qtw

class MyWidget(qtw.QWidget):
    def __init__(self):
        super().__init__()

        # Create a table widget with 4 rows and 3 columns
        self.table = qtw.QTableWidget(4, 3, self)
        self.table.setGeometry(10, 10, 300, 200)

        # Add a rank column with dropdown menus to the table
        self.rank_boxes = []
        for i in range(self.table.rowCount()):
            rank_box = qtw.QComboBox()
            rank_box.addItems([str(j+1) for j in range(self.table.rowCount())])
            self.table.setCellWidget(i, 2, rank_box)
            self.rank_boxes.append(rank_box)

        # Create a button to add rows to the table
        self.button = qtw.QPushButton('Add Row', self)
        self.button.setGeometry(10, 220, 100, 30)
        self.button.clicked.connect(self.add_row)

    def add_row(self):
        # Get the current row count and add a new row to the table
        current_row_count = self.table.rowCount()
        self.table.setRowCount(current_row_count + 1)

        # Create a rank dropdown menu for the new row
        row_count_options = [str(i+1) for i in range(current_row_count+1)]
        rank_box = qtw.QComboBox()
        rank_box.addItems(row_count_options)
        self.table.setCellWidget(current_row_count, 2, rank_box)
        self.rank_boxes.append(rank_box)

        # Update the items in the existing dropdown menus
        for box in self.rank_boxes:
            box.clear()
            box.addItems([str(i+1) for i in range(self.table.rowCount())])

if __name__ == '__main__':
    app = qtw.QApplication([])
    win = MyWidget()
    win.show()
    app.exec_()
