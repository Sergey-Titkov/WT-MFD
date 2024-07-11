import sys

from PyQt6 import QtCore
from PyQt6.QtCore import QSize, Qt, QObject, QThread
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from WarThunder import telemetry

# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Нам нужна нить для чтения данных из WT
        self.threadWT = QThread()
        # И объект который будем запускать
        self.browserWT = BrowserWT()
        # Перемещаем его в нить
        self.browserWT.moveToThread(self.threadWT)
        # after that, we can connect signals from this object to slot in GUI thread
        #self.browserHandler1.newTextAndColor.connect(self.addNewTextAndColor)
        # connect started signal to run method of object in another thread
        #self.thread1.started.connect(self.browserHandler1.run)
        # Запускаем нить
        self.threadWT.start()
        print('1')

        self.setWindowTitle("My App")
        button = QPushButton("Press Me!")

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(button)

class FirstMFDWindow(QMainWindow):
    def __init__(self):
        super().__init__()

class BrowserWT(QObject):
    running = False
    newTextAndColor = QtCore.pyqtSignal(str, object)
    telem = telemetry.TelemInterface()
    # method which will execute algorithm in another thread
    def do_work(self):
        print('Player:\t')
        while True:
            QtCore.QThread.msleep(100)
            print('Player:\t')
            # Забили пока на коменты и события
            if self.telem.get_telemetry(comments=False, events=False):

                pass


app = QApplication(sys.argv)

mainWindow = MainWindow()
mainWindow.show()

#firstMFDWindow = FirstMFDWindow()
#firstMFDWindow.show()

app.exec()