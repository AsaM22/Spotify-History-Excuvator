from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class AppWindow(QMainWindow):
    def __init__(self,):
        super(AppWindow, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.setGeometry(150,150, 500, 500)


if __name__ == "__main__":
        # App process
    app = QApplication(sys.argv)
    # Creates instance of the class
    win = AppWindow()
    
    # Shows Window
    win.show()
    # Quits app
    sys.exit(app.exec_())