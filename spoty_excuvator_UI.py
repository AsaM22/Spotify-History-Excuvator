# PyQt5 modules
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QCheckBox, QLabel, QMessageBox, QFileDialog, QScrollArea, QWidget, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys

# Files handling and counting
from json import load
from glob import glob1
from collections import Counter

# # Imports Scroll Label
# from custom_ScrollLabel import ScrollLabel


# TODO: 
# 6: Pyinstaller


class ScrollLabel(QScrollArea):
    """Creates a Scrollable Label"""

    def __init__(self, *args, **kwargs):
        """Constructor"""
        
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



class AppWindow(QMainWindow):
    """The window for Spoty Excuvator"""

    def __init__(self):
        """Initalizes UI"""
        
        # Calls super constructor
        super(AppWindow, self).__init__()

        # Calls Variable method
        self.initUIVar()

        # Calls UI method
        self.initUI()
        
        
    def initUIVar(self):
        """Initalizes variables for the widget position"""

        # Screen variables
        self.WINDOW_TITLE: str = "Spoty Excuvator"
        self.SCREEN_OFFSET_X: int = 175
        self.SCREEN_OFFSET_Y: int = 125     
        self.SCREEN_X: int = 950
        self.SCREEN_Y: int = 650

        # Button fonts
        self.BUTTON_FONT: str = 'Lucida Grande'

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
        self.DISPLAY_BUTTON_X: int = 210
        self.DISPLAY_BUTTON_Y: int = 400

        # File success label variables
        self.SUCCESS_LABEL_X: int = 350
        self.SUCCESS_LABEL_Y: int = 90
        
        # Total time label variables
        self.TOTAL_TIME_LABEL_X: int = 550
        self.TOTAL_TIME_LABEL_Y: int = 150

        # Scrollable label variables
        self.SCROLL_DISPLAY_X: int = 450
        self.SCROLL_DISPLAY_Y: int = self.TOTAL_TIME_LABEL_Y + 20
        self.SCROLL_DISPLAY_WIDTH: int = 400
        self.SCROLL_DISPLAY_HEIGHT: int = 475

        # ComboBox variables
        self.COMBOX_X: int = 215
        self.COMBOX_Y: int = 270
        self.COMBOX_WIDTH: int = 95
        self.COMBOX_HEIGHT: int = 25

        # Time converstion
        self.MS_SECONDS_FACTOR: float = .1
        self.MS_HOURS_FACTOR: float = 1/3600000
        self.MS_DAYS_FACTOR: float = 1/86400000

        # Sets default time
        self.played_time_option = 'Seconds'


    def initUI(self):
        """Creates widgets and sets properties"""

        # Setup screen
        self.setGeometry(self.SCREEN_OFFSET_X, self.SCREEN_OFFSET_Y, self.SCREEN_X, self.SCREEN_Y)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setStyleSheet("background-color: #DAD7D7;")


        # Setup select folder button
        self.directory_button = QPushButton('Select Downloaded Spotify Data Folder', self)
        self.directory_button.setFont(QFont(self.BUTTON_FONT, 18))
        self.directory_button.adjustSize()
        self.directory_button.move(int((self.SCREEN_X*.5) - (self.directory_button.size().width()*.5)), self.DIRECTORY_BUTTON_Y)
        self.directory_button.clicked.connect(self.select_file_btn)
        

        # Sets default path
        self.selected_directory_path = None


        # Setup Success Label
        self.success_label = QLabel("Selected Folder: Unsucessful", self)
        self.success_label.setStyleSheet("color: #F61313; font-size: 15px;")
        self.success_label.adjustSize()
        self.success_label.move(self.SUCCESS_LABEL_X, self.SUCCESS_LABEL_Y)


        # Setup Total time Label total_listened_ms_ms_ms
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
        self.display_button.move(self.DISPLAY_BUTTON_X, self.DISPLAY_BUTTON_Y)
        self.display_button.clicked.connect(self.file_display)


		# Creates Scroll label
        self.scroll_label = ScrollLabel(self)
        self.scroll_label.setGeometry(self.SCROLL_DISPLAY_X, self.SCROLL_DISPLAY_Y, self.SCROLL_DISPLAY_WIDTH, self.SCROLL_DISPLAY_HEIGHT)


        # ComboBox selector
        self.time_combox = QComboBox(self)
        self.time_combox.addItem("Seconds")
        self.time_combox.addItem("Hours")
        self.time_combox.addItem("Days")
        self.time_combox.setGeometry(self.COMBOX_X, self.COMBOX_Y, self.COMBOX_WIDTH, self.COMBOX_HEIGHT)
        self.time_combox.activated[str].connect(self.combox_update) 


    def cbx_update(self, state) -> None:
        """Makes sure only 1 checkbox is selected at a time"""

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
            
    
    def combox_update(self, selected) -> None:
        self.played_time_option = selected


    def show_warning(self, input_text: str = "Warning") -> None:
        """Displays a message box with Warning Icon

        Args:
            input_text (str): text to be displayed (default text is: "Warning")
        """
        
        # Creates MessageBox object
        message_box = QMessageBox()

        # Sets window title
        message_box.setWindowTitle("Warning!")

        # Sets Warning icon
        message_box.setIcon(QMessageBox.Warning)

        # Sets text to input text
        message_box.setText(input_text)

        # Displays message box
        message_box.exec_()


    def select_file_btn(self) -> None:
        """Opens File Dialog and sets directory path"""

        # Lets user select a path to data folder
        self.selected_directory_path = QFileDialog.getExistingDirectory(self, 'Select Spotify Data Folder')

        # Updates the file successfully found label
        if self.selected_directory_path:
            self.success_label.setStyleSheet("color: green; font-size: 15px;")
            self.success_label.setText("Selected Folder: Sucessful!")


    def file_display(self) -> None:
        """Gets and displays data"""
        
        # Checks if Folder and Checkbox have been selected
        if self.selected_directory_path == None:
            self.show_warning("Please select a folder")

        elif not (self.option1_cbx.isChecked() or self.option2_cbx.isChecked() or self.option3_cbx.isChecked() or self.option4_cbx.isChecked()):
            self.show_warning("Please select a checkbox")
        
        else:    
            def dict_count_sort(input_list: list) -> dict:
                """Sorts the dict based on second element (asending)"""
                return {k: v for k, v in sorted(Counter(input_list).items(), key=lambda item: item[1])} 

            def update_total_time(input_time_ms: float) -> None:
                """Updates the total time label"""
                self.total_time_label.setText(f"Total time listened: {input_time_ms/3600000:.2f} Hours")      
                self.total_time_label.adjustSize()            

            def scroll_print(input_list: list) -> None:
                """Updates text for scroll label"""
                temp_str = "".join(str(i) + "\n" for i in input_list)
                self.scroll_label.setText(temp_str.rstrip('\n'))


            # Finds the total number of StreamingHistory files
            file_count = len(glob1(self.selected_directory_path, "StreamingHistory*.json"))

            # Checks if the files exist
            if file_count == 0:
                self.show_warning("Please make sure to select the correct folder")

            # Initalizes a list to append all the songs
            myList = list()
            # Initalizes a dict for sorted data
            time_data = dict()
            # Initalizes total listen time
            total_listened_ms = 0

            # Loops through the amout of files you have (example: 4 loops)
            for count in range(file_count):
                # Changes file path
                _file_path = f"{self.selected_directory_path}/StreamingHistory{str(count)}.json"

                # Gets the raw json data
                with open(_file_path, "r" , encoding="utf8") as f:
                    data = load(f)

                # Loop through data and add to total_listened_ms
                for i in data:
                    total_listened_ms += i['msPlayed']


                # Append based on the selected choice
                if self.option1_cbx.isChecked():
                    for i in data:
                        myList.append(i['artistName']) 

                elif self.option2_cbx.isChecked():
                    for i in data:
                        myList.append(f"{i['artistName']}  ---  {i['trackName']}")                

                elif self.option3_cbx.isChecked():
                    for i in data:
                        myList.append(f"{i['trackName']}  ---  {i['artistName']}")
                        
                elif self.option4_cbx.isChecked():
                    # Creates elements in the dict for each artist with default value to avoid repeats
                    for i in data:
                        time_data[i['artistName']] = 0

                    # Loops over all records, converts then adds the artist played time 
                    for i in data:
                        if self.played_time_option == 'Seconds':
                            time_data[i['artistName']] = round(time_data[i['artistName']] + (i['msPlayed'] * self.MS_SECONDS_FACTOR))  
                        elif self.played_time_option == 'Hours':
                            time_data[i['artistName']] = round(time_data[i['artistName']] + (i['msPlayed'] * self.MS_HOURS_FACTOR), 3)
                        elif self.played_time_option == 'Days':
                            time_data[i['artistName']] = round(time_data[i['artistName']] + (i['msPlayed'] * self.MS_DAYS_FACTOR), 6)
                    
                    # TODO: Needs to only show 2-3 decimal points


            # Updates the total time listened label
            update_total_time(total_listened_ms)
            

            # Print the time related data
            if self.option1_cbx.isChecked() or self.option2_cbx.isChecked() or self.option3_cbx.isChecked():
                
                # Sorts and Counts how many of each song is played
                sorted_data = dict_count_sort(myList)

                # Creates a list of strings
                temp_lst = [str(sorted_data[i]) + " - " + i for i in sorted_data]

                # Print to Scroll label
                scroll_print(temp_lst)

            elif self.option4_cbx.isChecked():
                # Sorts the dict (asending)
                time_data = dict_count_sort(time_data)

                # Creates a list of strings
                temp_lst = [str(time_data[i]) + " --- " + i for i in time_data]

                # Print to Scroll label
                scroll_print(temp_lst)
        

if __name__ == "__main__":
    # Starts app process
    app = QApplication(sys.argv)
    # Creates instance of the class
    win = AppWindow()
    
    # Shows Window
    win.show()

    # Quits app correctly
    sys.exit(app.exec_())
