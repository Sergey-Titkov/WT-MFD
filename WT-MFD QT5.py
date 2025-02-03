import sys
import pygame
from lxml import etree
from PyQt5 import QtCore, QtWidgets, QtSvg
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextBrowser, QSizePolicy, QWidget
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
            result = None
            if self.telem.get_telemetry(comments=False, events=False):
                result = self.telem
                print('BrowserWT')

            self.telemetrySignal.emit(result)

# Окно для показа на MFD
class MFDWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MFDWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)                        # +++ Qt.Window
        self.setWindowTitle("MFD ONE")
        self.svgWidget = QtSvg.QSvgWidget(self)
        fileSVG = './MFD - 01___.svg'
        self.svgWidget.load(fileSVG)
        self.svgRoot = etree.parse(fileSVG)
        svg = etree.ETXPath("//{http://www.w3.org/2000/svg}svg")(self.svgRoot)
        width = int(svg[0].get('width'))
        height = int(svg[0].get('height'))
        # Устанавливаем размеры
        self.svgWidget.setGeometry(0, 0, width, height)
        self.svgWidget.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.setFixedSize(width, height)

    def updateMFD(self, object):
        if object:
            indicators = etree.ETXPath("//{http://www.w3.org/2000/svg}text[starts-with(@id,'sens_')]")(self.svgRoot);
            for indicator in indicators:
                name = indicator.get('id').replace('sens_', '')
                value = object.full_telemetry[name]
                indicator.text = '{}'.format(value)
                if name == 'mach':
                    if value < 0:
                        value = 0
                    indicator.text = '{:1.2f}'.format(value)
                if name == 'compass':
                    indicator.text = '{:.0f}'.format(value)

        else:
            print('None')
            indicators = etree.ETXPath("//{http://www.w3.org/2000/svg}text[starts-with(@id,'sens_')]")(self.svgRoot);
            for indicator in indicators:
                indicator.text = ''
        self.svgWidget.load(etree.tostring(self.svgRoot))

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

        # Создаем окно для MFD
        self.mfdWindow = MFDWindow(self)
        self.mfdWindow.resize(300, 300)
        self.mfdWindow.show()


    @QtCore.pyqtSlot(object)
    def telemetryProcessor(self, object):
        self.textBrowser.setTextColor(QColor(0, 0, 0))
        if object:
            pass
        else:
            self.textBrowser.append('None')
        self.mfdWindow.updateMFD(object)

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