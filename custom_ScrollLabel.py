from PyQt5.QtWidgets import QLabel, QScrollArea, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt



class ScrollLabel(QScrollArea):
	def __init__(self, *args, **kwargs):
		QScrollArea.__init__(self, *args, **kwargs)

		# Makes widget resizable
		self.setWidgetResizable(True)

		# Creates qwidget object
		content = QWidget(self)
		self.setWidget(content)

		# Creates Vertical box layout
		lay = QVBoxLayout(content)

		# Creates label
		self.label = QLabel(content)

		# Sets alignment to the text
		self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

		# Makes label multi-line
		self.label.setWordWrap(True)

		# Adds label to the layout
		lay.addWidget(self.label)

	# Creates setText method
	def setText(self, text):
		# setting text to the label
		self.label.setText(text)
