import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *
import threading


class TheThread(threading.Thread):
    def __init__(self, task, num, obj):
        threading.Thread.__init__(self)
        self.task = task
        self.num  = num
        self.obj  = obj

    def run(self):
        for i in range(self.num, 100):
            QtCore.QMetaObject.invokeMethod(
                self.obj,
                "onTask{}".format(self.task),
                QtCore.Qt.QueuedConnection,
                QtCore.Q_ARG(str, "Задача {}".format(self.task)),
                QtCore.Q_ARG(str, str(i))
                )
            QtCore.QThread.msleep(200)
        QtCore.QMetaObject.invokeMethod(
            self.obj,
            "onTask{}".format(self.task),
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(str, "Задача {}".format(self.task)),
            QtCore.Q_ARG(str, "End")
            )


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.label   = QLabel()
        self.label.setGeometry(QtCore.QRect(400, 450, 200, 100))
        self.label_2 = QLabel()
        self.label_2.setGeometry(QtCore.QRect(750, 450, 200, 100))
        self.cams = None

    def initUI(self):
        self.btn1 = QPushButton("Button 1", self)
        self.btn1.move(30, 50)
        self.btn1.clicked.connect(self.playGif)
        self.setGeometry(525, 100, 290, 150)
        self.setWindowTitle("Event sender")

    def buttonClicked(self):
        threading.Thread(target = self.playGif).start()

    def playGif(self):
        self.cams = WindowGif(self)
        self.cams.show()
        self.btn1.setEnabled(False)

    def closeEvent(self, event):
        if self.cams:
            self.cams.hide()
        self.label.hide()
        self.label_2.hide()
        super(Example, self).closeEvent(event)

    @QtCore.pyqtSlot(str, str)
    def onTask1(self, title, text):
        self.label.setText("{} - {}".format(title, text))
        self.label.show()
        if text=="End": self.btn1.setEnabled(True)

    @QtCore.pyqtSlot(str, str)
    def onTask2(self, title, text):
        self.label_2.setText("{} - {}".format(title, text))
        self.label_2.show()


class WindowGif(QDialog):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.movie_screen = QLabel(self)
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint |
                            Qt.MSWindowsFixedSizeDialogHint)
        self.movie_screen.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.movie_screen.setAttribute(Qt.WA_TranslucentBackground)
        self.movie = QMovie("loading.gif")
        self.movie_screen.setMovie(self.movie)
        self.movie.start()
        self.movie_screen.adjustSize()


# ff1 = f1()
# ff2 = f2()
#   Thread(target = ff1.func1()).start()
#   Thread(target = ff2.func2()).start()

        self.threadClass = TheThread(1, 10, self.parent)
        self.threadClass.start()

        self.threadClass2 = TheThread(2, 55, self.parent)
        self.threadClass2.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())