from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableView, QStandardItemModel, QComboBox

app = QApplication([])

# create a table view
table_view = QTableView()

# create a model for the table view
model = QStandardItemModel()
model.setColumnCount(2)
model.setHeaderData(0, Qt.Horizontal, "Column 1")
model.setHeaderData(1, Qt.Horizontal, "Column 2")

# add rows to the model
for i in range(5):
    row = [f"Row {i+1}", None]
    model.appendRow([QStandardItem(col) for col in row])

    # create a combobox for the second column
    combobox = QComboBox()
    combobox.addItems([str(i+1) for i in range(model.rowCount())])

    # set the combobox as the editor for the second column
    table_view.setItemDelegateForColumn(1, combobox)

# set the model for the table view
table_view.setModel(model)

# show the table view
table_view.show()

app.exec_()