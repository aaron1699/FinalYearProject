import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

class ViewHandler:
    def __init__(self, view):
        self.view = view

    def reset_view(self):
        self.view.table.setRowCount(0)
        self.view.table.showColumn(0)
        self.view.table.hideColumn(1)
        self.view.table.hideColumn(2)
        self.view.table.hideColumn(3)
        self.view.answer_here.hide()
        self.view.table.hide()
        self.view.answerExplanation.hide()
        self.view.answerExplanationInput.hide()
        self.view.addAnswerstoImageButton.hide()
        self.view.addRowButton.hide()

        try:
            self.view.addRowButton.disconnect()
        except Exception:
            pass

    def setup_common_elements(self):
        self.view.answer_here.show()
        self.view.table.show()
        self.view.answerExplanation.show()
        self.view.answerExplanationInput.show()
        self.view.addRowButton.show()
        self.view.imageButton.show()

    #setup views for those that have a fixed number of columns and rows

    def numericSetup(self):
        self.view.table.setRowCount(5)
        self.view.table.showColumn(2)
        self.view.addRowButton.hide()
        self.minLabel = qtw.QTableWidgetItem()
        self.minLabel = qtw.QLabel("Minimum Value")
        self.view.table.setCellWidget(0,0,self.minLabel)

        self.maxLabel = qtw.QTableWidgetItem()
        self.maxLabel = qtw.QLabel("Maximum Value")
        self.view.table.setCellWidget(1,0,self.maxLabel)

        self.decimalPlaces = qtw.QTableWidgetItem()
        self.decimalPlaces = qtw.QLabel("Decimal Places")
        self.view.table.setCellWidget(2,0,self.decimalPlaces)

        self.correctAnswer = qtw.QTableWidgetItem()
        self.correctAnswer = qtw.QLabel("Correct Answer")
        self.view.table.setCellWidget(3,0,self.correctAnswer)

        self.errorMargin = qtw.QTableWidgetItem()
        self.errorMargin = qtw.QLabel("Error Margin")
        self.view.table.setCellWidget(4,0,self.errorMargin)

    def xyPlotSetup(self):
        self.view.table.setRowCount(4)
        self.xText = qtw.QTableWidgetItem()
        self.xText = qtw.QLabel("Horizontal X axis")
        self.view.table.setCellWidget(0,0,self.xText)

        self.yText = qtw.QTableWidgetItem()
        self.yText = qtw.QLabel("vertical Y axis")
        self.view.table.setCellWidget(1,0,self.yText)

        self.maxX = qtw.QTableWidgetItem()
        self.maxX = qtw.QLabel("Max X value")
        self.view.table.setCellWidget(2,0,self.maxX)

        self.maxY = qtw.QTableWidgetItem()
        self.maxY = qtw.QLabel("Max Y value")
        self.view.table.setCellWidget(3,0,self.maxY)

    #define views

    def MCQView(self):
        self.reset_view()
        self.setup_common_elements()
        self.view.table.showColumn(1)
        self.view.table.showColumn(2)
        self.view.addRowButton.clicked.connect(self.addRowMCQ)

    def wordCloudView(self):
        self.reset_view()
    def textQuestionView(self):
        self.reset_view()
        self.setup_common_elements()
        self.view.table.showColumn(2)
        self.view.addRowButton.clicked.connect(self.addRowTXT)
    def rankingPreferenceView(self):
        self.reset_view()
        self.setup_common_elements()
        self.view.table.showColumn(2)
        self.view.addRowButton.clicked.connect(self.addRowTXT)
    def rankingOrderingView(self):
        self.reset_view()
        self.setup_common_elements()
        self.view.table.showColumn(2)
        self.view.table.showColumn(3)
        self.view.addRowButton.clicked.connect(self.addRowORD)
    def numericView(self):
        self.reset_view()
        self.setup_common_elements()
        self.view.table.setRowCount(5)
        self.numericSetup()
    def ratingView(self):
        self.reset_view()
    def xyPlotView(self):
        self.reset_view()
        self.setup_common_elements()
        self.view.table.showColumn(2)
        self.view.addRowButton.clicked.connect(self.addRowTXT)
        self.xyPlotSetup()
    def pinOnImageView(self):
        self.reset_view()
        self.view.answerExplanation.show()
        self.view.answerExplanationInput.show()
        self.view.addAnswerstoImageButton.show()
        self.view.imageButton.hide()
        


    def showhide(self, text):
        view_switcher = {
            'MultipleChoice': self.MCQView,
            'Word Cloud': self.wordCloudView,
            'Text Question': self.textQuestionView,
		    'Ranking By Preference': self.rankingPreferenceView,
		    'Ranking By Order': self.rankingOrderingView,
		    'Numeric': self.numericView,
		    'Rating': self.ratingView,
		    'XY Plot': self.xyPlotView,
		    'Pin on Image': self.pinOnImageView
        }

        if text in view_switcher:
            view_switcher[text]()



    

    def addRowMCQ(self):
        row = self.view.table.rowCount()
        self.view.table.insertRow(row)
        chkBoxItem = qtw.QTableWidgetItem()
        chkBoxItem.setFlags(qtc.Qt.ItemIsUserCheckable | qtc.Qt.ItemIsEnabled)
        chkBoxItem.setCheckState(qtc.Qt.Unchecked)       
        self.view.table.setItem(row,1,chkBoxItem)

        self.deleteAnswerButton = qtw.QTableWidgetItem()
        self.deleteAnswerButton = qtw.QPushButton("Delete")
        self.deleteAnswerButton.clicked.connect(self.deleteAnswer)
        self.view.table.setCellWidget(row,2,self.deleteAnswerButton)

    

    def addRowTXT(self):
        row = self.view.table.rowCount()
        self.view.table.insertRow(row)
		
        self.deleteAnswerButton = qtw.QTableWidgetItem()
        self.deleteAnswerButton = qtw.QPushButton("Delete")
        self.deleteAnswerButton.clicked.connect(self.deleteAnswer)
        self.view.table.setCellWidget(row,2,self.deleteAnswerButton)

    def addRowORD(self):
        row = self.view.table.rowCount()
        self.view.table.insertRow(row)
        self.rank_boxes = []
        for i in range(self.view.table.rowCount()):
            rank_box = qtw.QComboBox()
            rank_box.addItems([str(j+1) for j in range(self.view.table.rowCount())])
            self.view.table.setCellWidget(i, 2, rank_box)
            self.rank_boxes.append(rank_box)

	    # Create a rank dropdown menu for the new row
        row_count_options = [str(i+1) for i in range(row+1)]
        self.rank_box = qtw.QComboBox()
        self.rank_box.addItems(row_count_options)
        self.view.table.setCellWidget(row, 2, self.rank_box)
        self.rank_boxes.append(self.rank_box)
		

	    # Update the items in the existing dropdown menus
        for box in self.rank_boxes:
            box.clear()
            box.addItems([str(i+1) for i in range(self.view.table.rowCount())])
			

        self.deleteAnswerButton = qtw.QTableWidgetItem()
        self.deleteAnswerButton = qtw.QPushButton("Delete")
        self.deleteAnswerButton.clicked.connect(self.deleteAnswer)
        self.view.table.setCellWidget(row,3,self.deleteAnswerButton)

    def deleteAnswer(self):
        button = self.view.sender()
        if button:
            row = self.view.table.indexAt(button.pos()).row()
            self.view.table.removeRow(row)