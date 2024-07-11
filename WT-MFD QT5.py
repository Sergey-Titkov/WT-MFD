import sys
import time
import pygame

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextBrowser, QLabel, QWidget
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QObject, QThread
from WarThunder import telemetry

# Класс для получения телеметрии из WT
class BrowserWT(QObject):
    telem = telemetry.TelemInterface()
    def run(self):
        while True:
            QtCore.QThread.msleep(100)
            # Пока без событий и чата
            if self.telem.get_telemetry(comments=False, events=False):
                print('BrowserWT')

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

        # Создаем нить
        self.threadWT = QThread()
        # Создаем обработчик
        self.browserWT = BrowserWT()
        # Перемещаем обработчик в нить
        self.browserWT.moveToThread(self.threadWT)
        # Указываем нити какой метод из обработчика запустить
        self.threadWT.started.connect(self.browserWT.run)
        # Запускаем
        self.threadWT.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exit(app.exec_())