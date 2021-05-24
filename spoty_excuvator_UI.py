from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import sys

import json
from collections import Counter
import glob


class AppWindow(QMainWindow):
    def __init__(self):
        # Calls super constructor
        super(AppWindow, self).__init__()

        # Creates screen variables
        self.window_title: str = "Spoty Excuvator"
        self.screen_offset_x: int = 150
        self.screen_offset_y: int = 150     
        self.screen_x: int = 900
        self.screen_y: int = 600

        # Calls UI method
        self.initUI()
        

    def initUI(self):
        # Sets up screen
        self.setGeometry(self.screen_offset_x, self.screen_offset_y, self.screen_x, self.screen_y)
        self.setWindowTitle(self.window_title)
        
        self.directory_button = QPushButton('Select Folder', self)
        self.directory_button.adjustSize()
        self.directory_button.move((self.screen_x*.5) - (self.directory_button.size().width()*.5), 50)
        self.directory_button.clicked.connect(self.select_file_btn)



    def file_calculate(self):
        
        ###################### CHANGE THIS NUMBER FROM (0-2) ###################### 
        METHOD = 0      # TODO: Change this so that it is in an application
        # 0: Artist 		(Most played artist)
        # 1: Track/Artist 	(Track then Artist)
        # 2: Artist/Tarck	(Artist then Track)


        # Creates a list to append all the songs to
        myList = list()

        # Finds the total number of StreamingHistory files
        file_count = len(glob.glob1(self.folderpath, "StreamingHistory*.json"))


        # Loops through the amout of files you have (example: 4 loops)
        for count in range(file_count):

            # Changes file path
            _file_path = f"{self.folderpath}/StreamingHistory{str(count)}.json"

            # Gets the raw json data
            with open(_file_path, encoding="utf8") as f:
                data = json.load(f)


            # Append based on the selected choice
            for i in data:
                if METHOD == 0: myList.append(i["artistName"])
                elif METHOD == 1: myList.append(f"{i['trackName']}  ---  {i['artistName']}")
                elif METHOD == 2: myList.append(f"{i['artistName']}  ---  {i['trackName']}")


        # Counts how many of each song is played
        counted_data = Counter(myList)

        # Sorts the list (asending)
        sorted_data = {k: v for k, v in sorted(counted_data.items(), key=lambda item: item[1])}


        # Displays the sorted list (#TimesPlayed/Artist/SongTitle)
        for i in sorted_data:
            print(sorted_data[i], "-", i)



    def select_file_btn(self):
        # Lets user select a path to data folder
        self.selected_directory_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Spotify Data Folder')


if __name__ == "__main__":
    # Starts app process
    app = QApplication(sys.argv)
    # Creates instance of the class
    win = AppWindow()
    
    # Shows Window
    win.show()
    # Quits app
    sys.exit(app.exec_())
