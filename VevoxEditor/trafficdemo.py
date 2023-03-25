import sys
import math

from collections import namedtuple

import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

import shapely._geometry as sg


TrafficItem = namedtuple('TrafficItem', ['category', 'x', 'y', 'width', 'height'])

class MainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/gui.ui", self)
        self.addCarButton.clicked.connect(self.onAddCarButtonClicked)
        self.addPersonButton.clicked.connect(self.onAddPersonButtonClicked)
        self.addVanButton.clicked.connect(self.onAddVanButtonClicked)
        self.deleteButton.clicked.connect(self.onDeleteButtonClicked)
        self.deleteAllButton.clicked.connect(self.onDeleteAllButtonClicked)

        self.input_pixmap = QtGui.QPixmap("assets/base.png")
        self.output_pixmap = QtGui.QPixmap("assets/base.png")

        self.init_coords = (None, None)
        self.items = []
        self.tool = None
        self.tool_buttons = [self.addCarButton, self.addPersonButton, self.addVanButton, self.deleteButton]
        self.redraw()


    def widget2input(self, x, y):
        x_ret = x-self.inputLabel.x()
        y_ret = y-self.inputLabel.y()
        if x_ret < 0 or x_ret>= self.input_pixmap.width():
            x_ret = y_ret = None
        elif y_ret < 0 or y_ret>= self.input_pixmap.height():
            x_ret = y_ret = None
        return x_ret, y_ret

    def mousePressEvent(self, event):
        self.init_coords = self.widget2input(event.pos().x(), event.pos().y())
        self.updateAndRedraw()
    
    def mouseReleaseEvent(self, event):
        # Get end_coords
        self.end_coords = self.widget2input(event.pos().x(), event.pos().y())
        if self.end_coords[0] is None or self.end_coords[1] is None:
            return
        # Transform init and end coords into x, y, width and height
        x = min(self.init_coords[0], self.end_coords[0])
        y = min(self.init_coords[1], self.end_coords[1])
        width = int(math.fabs(self.init_coords[0]-self.end_coords[0]))
        height = int(math.fabs(self.init_coords[1]-self.end_coords[1]))
        print(x, y, width, height)
        if self.tool is None:
            pass
        elif self.tool == 'add_car':
            self.items.append(TrafficItem(category="car", x=x, y=y, width=width, height=height))
        elif self.tool == 'add_person':
            self.items.append(TrafficItem(category="person", x=x, y=y, width=width, height=height))
        elif self.tool == 'add_van':
            self.items.append(TrafficItem(category="van", x=x, y=y, width=width, height=height))
        elif self.tool == 'delete':
            self.delete_items(x, y, width, height)
        else:
            print(f'Unhandled tool {self.tool}')
            sys.exit(-1)
        self.updateAndRedraw()
    
    def redraw(self):
        self.inputLabel.setPixmap(self.input_pixmap)
        self.outputLabel.setPixmap(self.output_pixmap)

    def updateAndRedraw(self):
        output = self.THE_FUNCTION()
        image = QtGui.QImage(output.data, output.shape[1], output.shape[0], output.shape[1]*3, QtGui.QImage.Format.Format_RGB888)
        self.output_pixmap = QtGui.QPixmap(image)
        self.redraw()

    def THE_FUNCTION(self):
        output = np.zeros((480,640,3), dtype=np.uint8)
        for it in self.items:
            if it.category == "car":
                value = 160
            elif it.category == "van":
                value = 50
            elif it.category == "person":
                value = 255
            output[it.y:it.y+it.height, it.x:it.x+it.width, :] = value
        return output

    def onAddCarButtonClicked(self):
        for tool in self.tool_buttons:
            if tool != self.addCarButton:
                tool.setChecked(False)
        if self.addCarButton.isChecked():
            self.tool = 'add_car'
        else:
            self.tool = None
        print(self.tool)

    def onAddPersonButtonClicked(self):
        for tool in self.tool_buttons:
            if tool != self.addPersonButton:
                tool.setChecked(False)
        if self.addPersonButton.isChecked():
            self.tool = 'add_person'
        else:
            self.tool = None
        print(self.tool)

    def onAddVanButtonClicked(self):
        for tool in self.tool_buttons:
            if tool != self.addVanButton:
                tool.setChecked(False)
        if self.addVanButton.isChecked():
            self.tool = 'add_van'
        else:
            self.tool = None
        print(self.tool)

    def onDeleteButtonClicked(self):
        for tool in self.tool_buttons:
            if tool != self.deleteButton:
                tool.setChecked(False)
        if self.deleteButton.isChecked():
            self.tool = 'delete'
        else:
            self.tool = None
        print(self.tool)

    def onDeleteAllButtonClicked(self):
        self.items = []
        self.updateAndRedraw()

    def delete_items(self, x, y, width, height):
        polygon = sg.Polygon([(x, y), (x+width, y), (x+width, y+height), (x, y+height)])
        new_items = []
        for o in self.items:
            other = sg.Polygon([(o.x, o.y), (o.x+o.width, o.y), (o.x+o.width, o.y+o.height), (o.x, o.y+o.height)])
            intersection = polygon.intersection(other)
            if intersection.area <= 0:
                new_items.append(o)
        self.items = new_items

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
