from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys

import json
from collections import Counter
import glob


class AppWindow(QMainWindow):
    def __init__(self):
        # Calls super constructor
        super(AppWindow, self).__init__()

        # Screen variables
        self.WINDOW_TITLE: str = "Spoty Excuvator"
        self.SCREEN_OFFSET_X: int = 150
        self.SCREEN_OFFSET_Y: int = 150     
        self.SCREEN_X: int = 900
        self.SCREEN_Y: int = 600

        # Avoids magic numbers
        self.CBX_OPTION_ARTIST: int = 0
        self.CBX_OPTION_TRACK_ARTIST: int = 1
        self.CBX_OPTION_ARTIST_TRACK: int = 2

        # Directory Button variables
        self.DIRECTORY_BUTTON_Y: int = 50

        # Checkbox variables
        self.CBX_X: int = 200
        self.CBX_Y_1: int = 150
        self.CBX_Y_2: int = 180
        self.CBX_Y_3: int = 210
        self.CBX_WIDTH: int = 100
        self.CBX_HEIGHT: int = 30


        # Calls UI method
        self.initUI()
        

    def initUI(self):
        # Setup screen
        self.setGeometry(self.SCREEN_OFFSET_X, self.SCREEN_OFFSET_Y, self.SCREEN_X, self.SCREEN_Y)
        self.setWindowTitle(self.WINDOW_TITLE)
        

        # Setup select folder button
        self.directory_button = QPushButton('Select Downloaded Spotify Data Folder', self)
        self.directory_button.setFont(QFont('Sans-serif', 18))
        self.directory_button.adjustSize()
        self.directory_button.move(int((self.SCREEN_X*.5) - (self.directory_button.size().width()*.5)), self.DIRECTORY_BUTTON_Y)
        self.directory_button.clicked.connect(self.select_file_btn)
        

        # Creates 3 checkboxes
        self.option1_cbx = QCheckBox("Most Played Artist", self)
        self.option1_cbx.setGeometry(self.CBX_X, self.CBX_Y_1, self.CBX_WIDTH, self.CBX_HEIGHT)
        self.option2_cbx = QCheckBox("Artist then Track", self)
        self.option2_cbx.setGeometry(self.CBX_X, self.CBX_Y_2, self.CBX_WIDTH, self.CBX_HEIGHT)
        self.option3_cbx = QCheckBox("Track then Artist", self)
        self.option3_cbx.setGeometry(self.CBX_X, self.CBX_Y_3, self.CBX_WIDTH, self.CBX_HEIGHT)
  

        # Calls update method to uncheck other boxes
        self.option1_cbx.stateChanged.connect(self.cbx_update)
        self.option2_cbx.stateChanged.connect(self.cbx_update)
        self.option3_cbx.stateChanged.connect(self.cbx_update)


        # Setup Display button
        self.display_button = QPushButton('Display Data', self)
        self.display_button.setFont(QFont('Times', 20))
        self.display_button.adjustSize()
        self.display_button.move(int((self.SCREEN_X*.5) - (self.display_button.size().width()*.5)), 350)
        self.display_button.clicked.connect(self.file_calculate)


    def cbx_update(self, state):
        # Checks if state is changed
        if state == Qt.Checked:
  
            # If cbx 1 is selected
            if self.sender() == self.option1_cbx:
  
                # Unchecks other boxes
                self.option2_cbx.setChecked(False)
                self.option3_cbx.setChecked(False)

                # Sets method selector variable
                self.selected_method = self.CBX_OPTION_ARTIST
  
            # If cbx 2 is selected
            elif self.sender() == self.option2_cbx:
  
                # Unchecks other boxes
                self.option1_cbx.setChecked(False)
                self.option3_cbx.setChecked(False)
  
                # Sets method selector variable
                self.selected_method = self.CBX_OPTION_TRACK_ARTIST

            # If cbx 3 is selected
            elif self.sender() == self.option3_cbx:
  
                # Unchecks other boxes
                self.option1_cbx.setChecked(False)
                self.option2_cbx.setChecked(False)

                # Sets method selector variable
                self.selected_method = self.CBX_OPTION_ARTIST_TRACK


    def select_file_btn(self):
        # Lets user select a path to data folder
        self.selected_directory_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Spotify Data Folder')


    def file_calculate(self):
        # Select which data to print
        METHOD = self.selected_method
        # 0: Artist 		(Most played artist)
        # 1: Track/Artist 	(Track then Artist)
        # 2: Artist/Tarck	(Artist then Track)


        # Creates a list to append all the songs to
        myList = list()

        # Finds the total number of StreamingHistory files
        file_count = len(glob.glob1(self.selected_directory_path, "StreamingHistory*.json"))


        # Loops through the amout of files you have (example: 4 loops)
        for count in range(file_count):

            # Changes file path
            _file_path = f"{self.selected_directory_path}/StreamingHistory{str(count)}.json"

            # Gets the raw json data
            with open(_file_path, encoding="utf8") as f:
                data = json.load(f)


            # Append based on the selected choice
            for i in data:
                if METHOD == self.CBX_OPTION_ARTIST: myList.append(i["artistName"])
                elif METHOD == self.CBX_OPTION_TRACK_ARTIST: myList.append(f"{i['trackName']}  ---  {i['artistName']}")
                elif METHOD == self.CBX_OPTION_ARTIST_TRACK: myList.append(f"{i['artistName']}  ---  {i['trackName']}")


        # Counts how many of each song is played
        counted_data = Counter(myList)

        # Sorts the list (asending)
        sorted_data = {k: v for k, v in sorted(counted_data.items(), key=lambda item: item[1])}


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
