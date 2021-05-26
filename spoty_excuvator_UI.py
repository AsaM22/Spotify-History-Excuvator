from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QCheckBox, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys

from json import load
from collections import Counter
from glob import glob1



class AppWindow(QMainWindow):
    def __init__(self):
        # Calls super constructor
        super(AppWindow, self).__init__()

        # Calls Variable method
        self.initVar()

        # Calls UI method
        self.initUI()
        
        
    def initVar(self):
        # Screen variables
        self.WINDOW_TITLE: str = "Spoty Excuvator"
        self.SCREEN_OFFSET_X: int = 150
        self.SCREEN_OFFSET_Y: int = 150     
        self.SCREEN_X: int = 900
        self.SCREEN_Y: int = 600

        # Button fonts
        self.BUTTON_FONT = 'Lucida Grande'

        # Directory button variables
        self.DIRECTORY_BUTTON_Y: int = 50

        # Checkbox variables
        self.CBX_X: int = 200
        self.CBX_Y_1: int = 150
        self.CBX_Y_2: int = self.CBX_Y_1 + 30
        self.CBX_Y_3: int = self.CBX_Y_2 + 30
        self.CBX_Y_4: int = self.CBX_Y_3 + 30
        self.CBX_WIDTH: int = 150
        self.CBX_HEIGHT: int = 30

        # Display button variables
        self.DISPLAY_BUTTON_Y: int = 400

        # File success label
        self.SUCCESS_LABEL_X: int = 350
        self.SUCCESS_LABEL_Y: int = 90
        
        # Total time label
        self.TOTAL_TIME_LABEL_X: int = 550
        self.TOTAL_TIME_LABEL_Y: int = 150


    def initUI(self):
        # Setup screen
        self.setGeometry(self.SCREEN_OFFSET_X, self.SCREEN_OFFSET_Y, self.SCREEN_X, self.SCREEN_Y)
        self.setWindowTitle(self.WINDOW_TITLE)


        # Setup select folder button
        self.directory_button = QPushButton('Select Downloaded Spotify Data Folder', self)
        self.directory_button.setFont(QFont(self.BUTTON_FONT, 18))
        self.directory_button.adjustSize()
        self.directory_button.move(int((self.SCREEN_X*.5) - (self.directory_button.size().width()*.5)), self.DIRECTORY_BUTTON_Y)
        self.directory_button.clicked.connect(self.select_file_btn)
        
        # Setup Success Label
        self.success_label = QLabel("Selected Folder: Unsucessful", self)
        self.success_label.adjustSize()
        self.success_label.move(self.SUCCESS_LABEL_X, self.SUCCESS_LABEL_Y)


        # Setup Total time Label total_listened
        self.total_time_label = QLabel("Total time listened: 0 hours", self)
        self.total_time_label.adjustSize()
        self.total_time_label.move(self.TOTAL_TIME_LABEL_X, self.TOTAL_TIME_LABEL_Y)


        # Creates 3 checkboxes
        self.option1_cbx = QCheckBox("Most Played Artist", self)
        self.option1_cbx.setGeometry(self.CBX_X, self.CBX_Y_1, self.CBX_WIDTH, self.CBX_HEIGHT)
        self.option2_cbx = QCheckBox("Artist then Track", self)
        self.option2_cbx.setGeometry(self.CBX_X, self.CBX_Y_2, self.CBX_WIDTH, self.CBX_HEIGHT)
        self.option3_cbx = QCheckBox("Track then Artist", self)
        self.option3_cbx.setGeometry(self.CBX_X, self.CBX_Y_3, self.CBX_WIDTH, self.CBX_HEIGHT)
        self.option4_cbx = QCheckBox("Time per Artist", self)
        self.option4_cbx.setGeometry(self.CBX_X, self.CBX_Y_4, self.CBX_WIDTH, self.CBX_HEIGHT)

  
        # Calls update method to uncheck other boxes
        self.option1_cbx.stateChanged.connect(self.cbx_update)
        self.option2_cbx.stateChanged.connect(self.cbx_update)
        self.option3_cbx.stateChanged.connect(self.cbx_update)
        self.option4_cbx.stateChanged.connect(self.cbx_update)


        # Setup Display button
        self.display_button = QPushButton('Display Data', self)
        self.display_button.setFont(QFont(self.BUTTON_FONT, 20))
        self.display_button.adjustSize()
        self.display_button.move(int((self.SCREEN_X*.5) - (self.display_button.size().width()*.5)), self.DISPLAY_BUTTON_Y)
        self.display_button.clicked.connect(self.file_calculate)


    def cbx_update(self, state):
        # Checks if state is changed
        if state == Qt.Checked:
  
            # If cbx 1 is selected
            if self.sender() == self.option1_cbx:
  
                # Unchecks other boxes
                self.option2_cbx.setChecked(False)
                self.option3_cbx.setChecked(False)
                self.option4_cbx.setChecked(False)
  
            # If cbx 2 is selected
            elif self.sender() == self.option2_cbx:
  
                # Unchecks other boxes
                self.option1_cbx.setChecked(False)
                self.option3_cbx.setChecked(False)
                self.option4_cbx.setChecked(False)

            # If cbx 3 is selected
            elif self.sender() == self.option3_cbx:
  
                # Unchecks other boxes
                self.option1_cbx.setChecked(False)
                self.option2_cbx.setChecked(False)
                self.option4_cbx.setChecked(False)
            
            # If cbx 4 is selected
            elif self.sender() == self.option4_cbx:
  
                # Unchecks other boxes
                self.option1_cbx.setChecked(False)
                self.option2_cbx.setChecked(False)
                self.option3_cbx.setChecked(False)
            

    def select_file_btn(self):
        # Lets user select a path to data folder
        self.selected_directory_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Spotify Data Folder')

        if self.selected_directory_path:
            self.success_label.setText("Selected Folder: Sucessful!")


    def file_calculate(self):

        def dict_sort(input_list: list) -> dict:
            # Sorts the dict based on second element (asending)
            return {k: v for k, v in sorted(Counter(input_list).items(), key=lambda item: item[1])}


        # Finds the total number of StreamingHistory files
        file_count = len(glob1(self.selected_directory_path, "StreamingHistory*.json"))

        # Initalizes a list to append all the songs
        myList = list()
        # Initalizes a dict for sorted data
        time_data = dict()
        # Initalizes total listen time
        self.total_listened = 0

    
        # Loops through the amout of files you have (example: 4 loops)
        for count in range(file_count):
            # Changes file path
            _file_path = f"{self.selected_directory_path}/StreamingHistory{str(count)}.json"

            # Gets the raw json data
            with open(_file_path, "r" , encoding="utf8") as f:
                data = load(f)

            # Loop through data and add to total_listened
            for i in data:
                self.total_listened += i["msPlayed"]


            # Append based on the selected choice
            if self.option1_cbx.isChecked():
                for i in data:
                    myList.append(i["artistName"])

            elif self.option2_cbx.isChecked:
                for i in data:
                    myList.append(f"{i['trackName']}  ---  {i['artistName']}")

            elif self.option3_cbx.isChecked:
                for i in data:
                    myList.append(f"{i['artistName']}  ---  {i['trackName']}")
                    

            elif self.option4_cbx.isChecked:
                # Creates elements in the dict for each artist with default value to avoid repeats
                for i in data:
                    time_data[i['artistName']] = 0

                # Loops over all records and adds the artist played time
                for i in data:
                    time_data[i['artistName']] = time_data[i['artistName']] + i['msPlayed']

                # Sorts the dict (asending)
                time_data = dict_sort(time_data)


        # Updates the total time label
        self.total_time_label.setText(f"Total time listened: {self.total_listened/3600000:.2f} Hours")      
        self.total_time_label.adjustSize()


        # Print the time related data
        if self.option4_cbx.isChecked:
            for i in time_data:
                print(time_data[i], " --- ", i)
        else:
            # Counts how many of each song is played
            sorted_data = dict_sort(myList)

            # Displays the sorted list (#TimesPlayed/Artist/SongTitle)
            for i in sorted_data:
                print(sorted_data[i], "-", i)



if __name__ == "__main__":
    # Starts app process
    app = QApplication(sys.argv)
    # Creates instance of the class
    win = AppWindow()
    
    # Shows Window
    win.show()

    # Quits app
    sys.exit(app.exec_())
