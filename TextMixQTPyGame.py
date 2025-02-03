import time
import contextlib
from PySide6.QtCore import QObject, Signal, Qt, QThread
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QApplication

with contextlib.redirect_stdout(None):
    import pygame

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600


class PygameWorker(QObject):
    send_image = Signal(QImage)

    def run(self):
        # Initialise screen
        pygame.init()

        screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT),
                                            pygame.OPENGL)

        # Fill background
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((250, 250, 250))

        # Display some text
        font = pygame.font.Font(None, 36)
        text = font.render("Hello There", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)

        # Blit everything to the screen
        screen.blit(background, (0, 0))

        while not QThread.currentThread().isInterruptionRequested():
            screen.blit(background, (0, 0))
            # Get the display image
            image_str = pygame.image.tostring(pygame.display.get_surface(), "RGB", False)
            buffer = QImage(image_str, DISPLAY_WIDTH, DISPLAY_HEIGHT, QImage.Format_RGB888)
            if buffer.isNull():
                print("Buffer is null")
                continue

            self.send_image.emit(buffer)
            time.sleep(0.1)
        print("Thread finished")


class PygameReceiver(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.pygame_worker = PygameWorker()
        self.pygame_worker.send_image.connect(self.update_image)
        self.pygame_worker_thread = QThread()
        self.pygame_worker.moveToThread(self.pygame_worker_thread)
        self.pygame_worker_thread.started.connect(self.pygame_worker.run)
        self.pygame_worker_thread.start()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.image_label)

    def update_image(self, image):
        qpixmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(qpixmap)

    def closeEvent(self, event):
        self.pygame_worker_thread.requestInterruption()
        self.pygame_worker_thread.quit()
        self.pygame_worker_thread.wait()
        QMainWindow.closeEvent(self, event)


if __name__ == "__main__":
    app = QApplication()
    window = PygameReceiver()
    window.show()
    app.exec()