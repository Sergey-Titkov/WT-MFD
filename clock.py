# importing required librarie
from WarThunder import telemetry
from WarThunder import mapinfo
from lxml import etree
import math
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5 import QtSvg


import pygame


class Base:
    pass


def comapre_base(base):
    return base.player_distance


class Window(QWidget):

    def __init__(self):
        super().__init__()

        # Готовим виджет со стрелкой
        #file_name = r'02 - QTWidget.svg'
        #self.root = etree.parse(file_name)
        #self.angle = etree.ETXPath("//{http://www.w3.org/2000/svg}text[@id='angle']")
        #self.arrow = etree.ETXPath("//{http://www.w3.org/2000/svg}g[@id='Arrow']")
        file_name = r'02 - QTWidget.svg'
        self.svgWidget = QtSvg.QSvgWidget()
        self.svgWidget.load(file_name)
        self.svgWidget.setGeometry(300, 300, 150, 200)
        self.svgWidget.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed))
        self.svgWidget.cstTarget = etree.ETXPath("//{http://www.w3.org/2000/svg}text[@id='select-target']")
        self.svgWidget.cstAngle = etree.ETXPath("//{http://www.w3.org/2000/svg}text[@id='angle']")
        self.svgWidget.cstArrow = etree.ETXPath("//{http://www.w3.org/2000/svg}g[@id='Arrow']")
        self.svgWidget.cstRoot = etree.parse(file_name)


        # Setup a timer event

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
        layout.addWidget(self.svgWidget)

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
        self.label1.setText(label_time)
        self.label2.setText(label_time)

        if self.telem.get_telemetry(comments=False, events=False):
#            print('Player:\t')
#           print('\tX и Y:\t{},{}'.format(self.telem.map_info.player_x, self.telem.map_info.player_y))
#            print('\tLat и Lon:\t{},{}'.format(self.telem.map_info.player_lat, self.telem.map_info.player_lon))
            grid_steps = self.telem.map_info.info['grid_steps']
            size_x = self.telem.map_info.info['map_max'][0] - self.telem.map_info.info['map_min'][0]
            size_y = self.telem.map_info.info['map_max'][1] - self.telem.map_info.info['map_min'][1]

            self.map_cell_size.setText('Клетка: {0:2.1f}х{1:2.1f}км'.format(grid_steps[0] / 1000, grid_steps[1] / 1000))

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

#                    print('\tBombing Point: {}, distance: {:2.1f}км, course: {:3.0f}'.format(bomb_point.name,
#                                                                                             bomb_point.player_distance / 1000,
#                                                                                             bomb_point.player_course))
#                else:
#                    print('\tNone')
#                print(' ')
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

            joystick = pygame.joystick.Joystick(2)
            if joystick:
                if joystick.get_button(13):
                    print("Кнопка 13")
                    if sorted_base:
                        self.current_base_index = self.current_base_index + 1
                        print('self.current_base_index {}'.format(self.current_base_index))
                        print('len(sorted_base) {}'.format(len(sorted_base)))
                        if self.current_base_index > len(sorted_base)- 1 :
                            self.current_base_index = 0
                            print('self.current_base_index {}'.format(self.current_base_index))
                        self.current_base = sorted_base[self.current_base_index]
                        print('self.current_base',self.current_base)

            if not sorted_base:
                self.current_base = None

            if sorted_base and self.current_base:
                for base in sorted_base:
                    if base.x == self.current_base.x and base.y == self.current_base.y:
                        self.current_base = base
            stroka = ''

            if self.current_base:
                stroka = '{} {:2.1f}км {:3.0f}°'.format(self.current_base.name,
                                                                        self.current_base.player_distance / 1000,
                                                                        self.current_base.player_course)
            self.label1.setText(stroka)
            course_angle = 0
            course_angle_text = ''
            if self.current_base:
                player_speed = int(self.telem.full_telemetry['speed'])
                # м/с
                if player_speed == 0:
                    time_arrival_stroka = '-'
                else:
                    time_arrival = int(self.current_base.player_distance/player_speed)
                    time_arrival_stroka = '{}'.format(time_arrival)
                    if time_arrival > 999:
                        time_arrival_stroka = '∞'
                stroka = '{} {:2.1f}км {}c'.format(self.current_base.name,
                                                self.current_base.player_distance / 1000,
                                                   time_arrival_stroka
                                                )
                base_course = int(self.current_base.player_course)
                base_course = base_course if base_course !=360 else 0

                player_course_begin = int(self.telem.full_telemetry['compass'])


                if player_course_begin > 180:
                    player_course_end = player_course_begin - 180
                else:
                    player_course_end = player_course_begin + 180
                player_course_end = player_course_end if player_course_end !=360 else 0

                if player_course_begin < 180:
                    if player_course_begin <= base_course and base_course <= player_course_end:
                        # Отработка доварота в +
                        course_angle = base_course - player_course_begin
                        course_angle_text = '+{}'.format(int(course_angle))
                    else:
                        # Отработка доварота в -
                        if base_course <= player_course_begin:
                            course_angle = player_course_begin - base_course
                        else:
                            course_angle = 360 - base_course + player_course_begin
                        course_angle_text = '-{}'.format(int(course_angle))
                        course_angle = 360 - course_angle
                else:
                    if base_course >= player_course_begin or ( 0< base_course and base_course <= player_course_end):
                        # Отработка доварота в +
                        if base_course >= player_course_begin:
                            # Мы в одной половинке
                            course_angle = base_course - player_course_begin
                        else:
                            course_angle = 360 - player_course_begin + base_course
                        course_angle_text = '+{}'.format(int(course_angle))
                    else:
                        course_angle = player_course_begin - base_course
                        course_angle_text = '-{}'.format(int(course_angle))
                        course_angle = 360 - course_angle



                course_angle_text = '{}'.format(course_angle_text, int(player_course_begin), int(base_course))
            self.svgWidget.cstTarget(self.svgWidget.cstRoot)[0].text = stroka
            self.svgWidget.cstAngle(self.svgWidget.cstRoot)[0].text = course_angle_text
            self.svgWidget.cstArrow(self.svgWidget.cstRoot)[0].set('transform', "rotate({},75,93)".format(int(course_angle)))
            #self.telem.full_telemetry['compass']
            self.svgWidget.load(etree.tostring(self.svgWidget.cstRoot))


# create pyqt5 app
pygame.init()

App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# showing all the widgets
window.show()

# start the app
App.exit(App.exec_())
