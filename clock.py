# importing required librarie
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime, Qt


class Window(QWidget):

    def __init__(self):
        super().__init__()

        # setting geometry of main window
        self.setGeometry(100, 100, 800, 400)

        # creating a vertical layout
        layout = QVBoxLayout()

        # creating font object
        font = QFont('Consolas', 14, QFont.Bold)

        # creating a label object
        self.map_cell_size = QLabel()
        self.label1 = QLabel()
        self.label2 = QLabel()

        # setting center alignment to the label
        self.map_cell_size.setAlignment(Qt.AlignCenter)
        self.label1.setAlignment(Qt.AlignCenter)
        self.label2.setAlignment(Qt.AlignCenter)

        # setting font to the label
        self.map_cell_size.setFont(font)
        self.label1.setFont(font)
        self.label2.setFont(font)

        # adding label to the layout
        layout.addWidget(self.map_cell_size)
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)

        # setting the layout to main window
        self.setLayout(layout)

        # creating a timer object
        timer = QTimer(self)

        # adding action to timer
        timer.timeout.connect(self.showTime)

        # update the timer every second
        timer.start(200)

    # method called by timer
    def showTime(self):
        # getting current time
        current_time = QTime.currentTime()

        # converting QTime object to string
        label_time = current_time.toString('hh:mm:ss')

        # showing it to the label
        grid_step_x = 13102.0
        grid_step_y = 13103.0
        self.map_cell_size .setText('Клетка: {0:2.1f}х{1:2.1f}км'.format(grid_step_x/1000,grid_step_y/1000))
        self.label1.setText(label_time)
        self.label2.setText(label_time)


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# showing all the widgets
window.show()

# start the app
App.exit(App.exec_())