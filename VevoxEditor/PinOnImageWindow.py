import math

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5 import uic


class PinOnImageWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("gui.ui", self)

        self.openFile()
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.doneButton.clicked.connect(self.close)
        self.input_pixmap = QtGui.QPixmap(self.fname)
        self.output_pixmap = QtGui.QPixmap(self.fname)

        self.init_coords = (None, None)
        self.end_coords = (None, None)
        self.items = []
        #self.tool = None
        #self.tool_buttons = [self.deleteButton]
        self.circles = [] # list to store circles
        self.redraw()
        self.correctItems = []

    
    
    def openFile(self):
        self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(
		    self, 'Open file', 'c:\\', "Image files (*.jpg *.gif *.png)")
        return

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

    def mouseMoveEvent(self, event):
        self.end_coords = self.widget2input(event.pos().x(), event.pos().y())
        self.updateAndRedraw()

    def mouseReleaseEvent(self, event):
        self.end_coords = self.widget2input(event.pos().x(), event.pos().y())
        if self.end_coords[0] is None or self.end_coords[1] is None:
            return
        # Transform init and end coords into x, y, width and height
        x = (self.init_coords[0] + self.end_coords[0]) / 2
        y = (self.init_coords[1] + self.end_coords[1]) / 2
        width = int(math.fabs(self.init_coords[0]-self.end_coords[0]))/2
        height = int(math.fabs(self.init_coords[1]-self.end_coords[1]))/2
        print(f"x: {x}, y: {y}, width: {width}, height: {height}")
        self.items.append((x, y, width, height))
        self.correctItems.append({"x": x/self.input_pixmap.width(), "y": y/self.input_pixmap.height(), "xRadius": width/self.input_pixmap.width(), "yRadius" :height/self.input_pixmap.height()})        
        self.updateAndRedraw()
        print(self.items)
        print(self.correctItems)

    def deleteButtonClicked(self):
        if self.items:
            self.items.pop()  # remove most recently drawn circle from list
            self.correctItems.pop()
            self.updateAndRedraw()

    #def doneButtonClicked(self):


    def THE_FUNCTION(self):
        output = self.input_image.copy()
        for circle in self.circles:
            x, y, r = circle
            self.circles.append((x, y, r)) # append to list
        return output, self.circles

    def redraw(self):
        self.inputLabel.setPixmap(self.input_pixmap)
        self.outputLabel.setPixmap(self.output_pixmap)

    def updateAndRedraw(self):
        self.drawOutput()
        self.redraw()

    def drawOutput(self):
        self.output_pixmap = self.input_pixmap.copy()
        painter = QtGui.QPainter(self.output_pixmap)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
        pen.setWidth(2)
        painter.setPen(pen)
        for item in self.items:
            x, y, rx, ry = item
            rect = QtCore.QRectF(x - rx, y - ry, 2 * rx, 2 * ry)
            painter.drawEllipse(rect)
        if self.init_coords[0] is not None and self.init_coords[1] is not None and \
                self.end_coords[0] is not None and self.end_coords[1] is not None:
            x = (self.init_coords[0] + self.end_coords[0]) / 2
            y = (self.init_coords[1] + self.end_coords[1]) / 2
            rx = math.fabs(self.init_coords[0] - self.end_coords[0]) / 2
            ry = math.fabs(self.init_coords[1] - self.end_coords[1]) / 2
            rect = QtCore.QRectF(x - rx, y - ry, 2 * rx, 2 * ry)
            painter.drawEllipse(rect)
        painter.end()

    