from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

import json
from collections import Counter
import glob


class AppWindow(QMainWindow):
    def __init__(self):
        super(AppWindow, self).__init__()
        self.initUI()
        

    def initUI(self):
        self.setGeometry(150,150, 500, 500)
        self.setWindowTitle("Display Streamed History")
        
        self.folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.show_history()

    def get_file(self):
        return self.folderpath

    def show_history(self):
        ###################### CHANGE THIS NUMBER FROM (0-2) ###################### 
        METHOD = 2      # TODO: Change this so that it is in an application
        # 0: Artist 		(Most played artist)
        # 1: Track/Artist 	(Track then Artist)
        # 2: Artist/Tarck	(Artist then Track)

        # Folder path with streaming history files in it
        folder_path = self.get_file()

        # Creates a list to append all the songs to
        myList = list()

        # Finds the total number of StreamingHistory files
        file_count = len(glob.glob1(folder_path, "StreamingHistory*.json"))


        # Loops through the amout of files you have (example: 4 loops)
        for count in range(file_count):

            # Changes file path
            _file_path = f"{folder_path}/StreamingHistory{str(count)}.json"

            # Gets the raw json data
            with open(_file_path) as f:
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

        # Ends the code
        exit()

        

def main():
    app = QApplication(sys.argv)
    win = AppWindow()

    win.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()