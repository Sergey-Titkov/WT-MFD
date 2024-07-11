import sys
import time
import pygame

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextBrowser, QLabel, QWidget
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QObject, QThread
from WarThunder import telemetry

# Класс для состояния джойстика
class BrowserJoysticks(QtCore.QObject):
    running = False
    joysticksSignal = QtCore.pyqtSignal(object)
    joysticksState = {}
    # method which will execute algorithm in another thread
    def run(self):
        pygame.init()
        joysticks = {}

        for i in range(0, pygame.joystick.get_count()):
           joy = pygame.joystick.Joystick(i)
           joy.init()
           joysticks[joy.get_instance_id()] = joy
           self.joysticksState[joy.get_name()] = '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
           print(joy.get_name(),' ',joy.get_instance_id())


        while True:
            QtCore.QThread.msleep(100)
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                   print("Кнопка ВКЛ: ", event.button,' ',joysticks[event.instance_id].get_name() )
                   tmp = self.joysticksState[joysticks[event.instance_id].get_name()]
                   result = tmp[:event.button] + '1' + tmp[event.button+1:]
                   self.joysticksState[joysticks[event.instance_id].get_name()] = result
                   print(joysticks[event.instance_id].get_name(), ": ", self.joysticksState[joysticks[event.instance_id].get_name()])
                   self.joysticksSignal.emit(self.joysticksState)

                if event.type == pygame.JOYBUTTONUP:
                   print("Кнопка ВЫКЛ: ", event.button, ' ', joysticks[event.instance_id].get_name())
                   tmp = self.joysticksState[joysticks[event.instance_id].get_name()]
                   result = tmp[:event.button] + '0' + tmp[event.button+1:]
                   self.joysticksState[joysticks[event.instance_id].get_name()] = result
                   print(joysticks[event.instance_id].get_name(), ": ", self.joysticksState[joysticks[event.instance_id].get_name()])


# Класс для получения телеметрии из WT
class BrowserWT(QObject):
    telem = telemetry.TelemInterface()
    telemetrySignal = QtCore.pyqtSignal(object)
    def run(self):
        while True:
            QtCore.QThread.msleep(100)
            # Пока без событий и чата
#            self.newTextAndColor.emit(
#                '{} - thread 2 variant 2.\n'.format(str(time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()))),
#                QColor(255, 0, 0)
#            )
            result = None
            if self.telem.get_telemetry(comments=False, events=False):
                result = self.telem
                print('BrowserWT')

            self.telemetrySignal.emit(result)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настраиваем окно
        self.setWindowTitle("WT-MFD")
        self.resize(500, 400)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QTextBrowser()
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)

        # Для QMainWindow обязательно нужно установить контейнер
        container = QWidget()
        container.setLayout(self.verticalLayout)
        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(container)

        # Обрабатываем телеметрию
        # Создаем нить
        self.threadWT = QThread()
        # Создаем обработчик
        self.browserWT = BrowserWT()
        # Перемещаем обработчик в нить
        self.browserWT.moveToThread(self.threadWT)
        # Связываем обработчики сигналов
        self.browserWT.telemetrySignal.connect(self.telemetryProcessor)
        # Указываем нити какой метод из обработчика запустить
        self.threadWT.started.connect(self.browserWT.run)
        # Запускаем
        self.threadWT.start()

        # Обрабатываем джойстик
        # Создаем нить
        self.threadJoy = QThread()
        # Создаем обработчик
        self.browserJoysticks = BrowserJoysticks()
        # Перемещаем обработчик в нить
        self.browserJoysticks.moveToThread(self.threadJoy)
        # Связываем обработчики сигналов
        self.browserJoysticks.joysticksSignal.connect(self.joysticksProcessor)
        # Указываем нити какой метод из обработчика запустить
        self.threadJoy.started.connect(self.browserJoysticks.run)
        # Запускаем
        self.threadJoy.start()


    @QtCore.pyqtSlot(object)
    def telemetryProcessor(self, object):
        self.textBrowser.setTextColor(QColor(0, 0, 0))
        if object:
            self.textBrowser.append('Что то есть')
        else:
            self.textBrowser.append('None')

    @QtCore.pyqtSlot(object)
    def joysticksProcessor(self, object):
        self.textBrowser.setTextColor(QColor(0, 255, 0))
        if object:
            for item in object:
                self.textBrowser.append('{}: {}'.format(item, object[item]))
        else:
            self.textBrowser.append('None')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exit(app.exec_())