# importing required librarie
from WarThunder import telemetry
from WarThunder import mapinfo
import math
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime, Qt


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.telem = telemetry.TelemInterface()

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

        if self.telem.get_telemetry(comments=False, events=False):
            print('Player:\t')
            print('\tX и Y:\t{},{}'.format(self.telem.map_info.player_x, self.telem.map_info.player_y))
            print('\tLat и Lon:\t{},{}'.format(self.telem.map_info.player_lat, self.telem.map_info.player_lon))
            grid_steps = self.telem.map_info.info['grid_steps']
            size_x = self.telem.map_info.info['map_max'][0] - self.telem.map_info.info['map_min'][0]
            size_y = self.telem.map_info.info['map_max'][1] - self.telem.map_info.info['map_min'][1]

            bomb_points = [obj for obj in self.telem.map_info.bombing_points() if not obj.friendly]
            stroka = ''
            if bomb_points:
                for bomb_point in bomb_points:
                    base_x = bomb_point.position[0]
                    base_y = bomb_point.position[1]
                    player_x = self.telem.map_info.player_x
                    player_y = self.telem.map_info.player_y
                    a = abs(player_y - base_y) * size_x
                    b = abs(player_x - base_x) * size_y
                    player_distance = math.sqrt(a * a + b * b)
                    quarter = 0
                    sign = 0
                    if player_x < base_x and player_y > base_y:
                        quarter = 90
                        sign = -1
                    else:
                        if player_x < base_x and player_y < base_y:
                            quarter = 90
                            sign = 1
                        else:
                            if player_x > base_x and player_y < base_y:
                                quarter = 270
                                sign = -1
                            else:
                                quarter = 270
                                sign = 1
                    if b == 0 and a == 0:
                        quarter = 90
                        alpha = 90
                        sign = -1
                    else:
                        if b == 0 and player_y > base_y:
                            quarter = 90
                            alpha = 90
                            sign = -1
                        else:
                            if a == 0 and player_x < base_x:
                                quarter = 90
                                alpha = 0
                                sign = -1
                            else:
                                if b == 0 and player_y < base_y:
                                    quarter = 90
                                    alpha = 90
                                    sign = 1
                                else:
                                    alpha = math.atan(a / b) * 180 / math.pi

                    player_course = quarter + sign * alpha
                    bomb_point.player_distance = player_distance
                    bomb_point.player_course = player_course

                    column = 1 + int(base_x * size_x / self.telem.map_info.info['grid_steps'][0])
                    row = chr(65 + int(base_y * size_y / self.telem.map_info.info['grid_steps'][1]))
                    name = '{}{}'.format(row, column)
                    bomb_point.name = name
                    print('\tBombing Point: {}, distance: {:2.1f}км, course: {:3.0f}'.format(bomb_point.name,
                                                                                             bomb_point.player_distance / 1000,
                                                                                             bomb_point.player_course))
                    stroka = stroka +'\n'+'Bombing Point: {}, distance: {:2.1f}км, course: {:3.0f}'.format(bomb_point.name,
                                                                                             bomb_point.player_distance / 1000,
                                                                                             bomb_point.player_course)

                else:
                    print('\tNone')
                print(' ')
                #time.sleep(0.2)
            else:
                pass

            self.label2.setText(stroka)
# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# showing all the widgets
window.show()

# start the app
App.exit(App.exec_())