# importing required librarie
from WarThunder import telemetry
from WarThunder import mapinfo
import math
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime, Qt

import pygame

class Base:
    pass


def comapre_base(base):
    return base.player_distance


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.current_base_index = 0
        self.current_base = None

        joysticks = []
        for i in range(0, pygame.joystick.get_count()):
            joysticks.append(pygame.joystick.Joystick(i))
            joysticks[-1].init()

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
        self.map_cell_size.setText('Клетка: {0:2.1f}х{1:2.1f}км'.format(grid_step_x / 1000, grid_step_y / 1000))
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
            self.base_list = []
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

                    base = Base()
                    base.name = name
                    base.x = base_x
                    base.y = base_y
                    base.player_distance = player_distance
                    base.player_course = player_course
                    self.base_list.append(base)

                    print('\tBombing Point: {}, distance: {:2.1f}км, course: {:3.0f}'.format(bomb_point.name,
                                                                                             bomb_point.player_distance / 1000,
                                                                                             bomb_point.player_course))
                else:
                    print('\tNone')
                print(' ')
                # time.sleep(0.2)
            else:
                pass
            stroka = ''
            sorted_base = []
            if self.base_list:
                sorted_base = sorted(self.base_list, key=comapre_base)
                for base in sorted_base:
                    stroka = stroka + '\n' + '{} {:2.1f}км {:3.0f}°'.format(base.name, base.player_distance / 1000,
                                                                            base.player_course)
            self.label2.setText(stroka)
            print('event')
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.JOYBUTTONUP and event.dict['joy'] == 1 and event.dict['button'] == 13 and sorted_base:
                    self.current_base_index = self.current_base_index + 1
                    if self.current_base_index - 1 > len(sorted_base):
                        self.current_base_index = 0
                    self.current_base = sorted_base.index(self.current_base_index)
            stroka = ''
            print('event_1')
            if self.current_base:
                stroka = stroka + '\n' + '{} {:2.1f}км {:3.0f}°'.format(self.current_base.name, self.current_base.player_distance / 1000,
                                                                        self.current_base.player_course)
            self.label1.setText(stroka)

# create pyqt5 app
pygame.init()

App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# showing all the widgets
window.show()

# start the app
App.exit(App.exec_())
