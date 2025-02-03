import sys
from PyQt5 import QtWidgets, QtCore                                 # + QtCore


class Window1(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Window1, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)                        # +++ Qt.Window
        label = QtWidgets.QLabel("Label 1")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

class Window2(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Window2, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)                        # +++ Qt.Window
        label = QtWidgets.QLabel("Label 2")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()

        window1_button = QtWidgets.QPushButton("Window 1")
        window2_button = QtWidgets.QPushButton("Window 2")

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(window1_button)
        layout.addWidget(window2_button)

        window1_button.clicked.connect(self.open_window1)
        window2_button.clicked.connect(self.open_window2)

    def open_window1(self):
        self.window = Window1(self)                                            # +++ self
        self.window.resize(300, 300)
        self.window.show()

    def open_window2(self):
        window = Window2(self)                                                  # +++ self
        window.resize(300, 300)
        window.show()

if __name__ == '__main__':
    application = QtWidgets.QApplication([])
    window = MainWindow()
    window.resize(500, 500)
    window.show()
    sys.exit(application.exec_())