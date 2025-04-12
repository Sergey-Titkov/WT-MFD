import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtCore import Qt, QSettings, QByteArray


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SVG Viewer")

        # Инициализация графических элементов
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        # Загрузка SVG-изображения
        self.renderer = QSvgRenderer("MFD - 01___.svg")
        if not self.renderer.isValid():
            raise ValueError("Ошибка загрузки SVG-файла")

        self.svg_item = QGraphicsSvgItem()
        self.svg_item.setSharedRenderer(self.renderer)
        self.scene.addItem(self.svg_item)

        # Установка размеров сцены
        svg_size = self.renderer.defaultSize()
        self.scene.setSceneRect(0, 0, svg_size.width(), svg_size.height())

        # Настройка отображения
        #self.view.setRenderHints(QGraphicsView.Antialiasing |                                 QGraphicsView.SmoothPixmapTransform)
        self.view.setAlignment(Qt.AlignCenter)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Загрузка настроек
        self.load_window_settings()

    def closeEvent(self, event):
        # Сохранение настроек перед закрытием
        self.save_window_settings()
        super().closeEvent(event)

    def load_window_settings(self):
        settings = QSettings("settings.ini", QSettings.IniFormat)
        geometry = settings.value("geometry", QByteArray())
        window_state = settings.value("window_state", Qt.WindowNoState)

        if geometry.isEmpty():
            self.resize(400, 300)
            self.center_window()
        else:
            self.restoreGeometry(geometry)

        self.setWindowState(Qt.WindowState(int(window_state)))

    def save_window_settings(self):
        settings = QSettings("settings.ini", QSettings.IniFormat)
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("window_state", int(self.windowState()))

    def center_window(self):
        # Центрирование окна на экране
        frame = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame.moveCenter(screen_center)
        self.move(frame.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())