import sys
import logging
from datetime import datetime
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtCore import Qt, QSettings, QByteArray, QObject, QThread
import xml.etree.ElementTree as ET
from WarThunder import telemetry

version = '0.0.1'

# Класс для получения телеметрии из WT
class BrowserWT(QObject):
    # Класс читающий телеметрию из WT
    TelemInterface = telemetry.TelemInterface()
    telemetrySignal = QtCore.pyqtSignal(object)
    def run(self):
        while True:
            QtCore.QThread.msleep(100)
            full_telemetry = None

            # Пока без событий и чата
            if self.TelemInterface.get_telemetry(comments=False, events=False):
                full_telemetry = self.TelemInterface.full_telemetry
                current_time=datetime.now()
                full_telemetry['clock_hour'] = current_time.hour
                full_telemetry['clock_min'] = current_time.minute
                full_telemetry['clock_sec'] = current_time.second
                full_telemetry['clock_microsecond'] = current_time.microsecond
            self.telemetrySignal.emit(full_telemetry)

class MainWindow(QMainWindow):
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    file_path = "main.svg"

    def updateMFD(self,telemetry):

        if not telemetry:
            self.svg_item.setVisible(False)
            return
        else:
            if not self.svg_item.isVisible():
                self.svg_item.setVisible(True)

        # Находим все элементы с атрибутом data-sensor-name во всем дереве
        elements = self.svg_root.findall('.//*[@data-sensor-name]', namespaces=self.namespaces)
        for indicator in elements:
            # Безопасно получаем атрибуты
            id = indicator.get('id', '').strip()
            sensor_name = indicator.get('data-sensor-name', '').strip()
            text_format = indicator.get('data-sensor-text-format', '').strip()

            # Имя сенсора должно быть задано
            if not sensor_name:
                continue
            # Обрабатываем только сенсоры у которых не было ошибок
            if sensor_name in self.sensor_has_error:
                continue
            # Если сенсора не нашли в телеметрии, то закидываем его в ошибочные
            if sensor_name not in telemetry:
                # Определяем, является ли элемент tspan
                tag_local = indicator.tag.split('}')[-1]  # Локальное имя тега без namespace
                print(indicator.tag)
                if tag_local == 'tspan':
                    # Скрываем родительский text
                    parent = indicator.getparent()
                    if parent is not None:
                        parent.set('display', 'none')
                else:
                    # Скрываем сам элемент
                    indicator.set('display', 'none')
                continue
                #self.sensor_has_error.append(sensor_name)
                #logging.warning(f'Параметр не найден: ID ={id} data-sensor-name={sensor_name}')
                #continue


            value = telemetry[sensor_name]

            try:
                indicator.text = f'{telemetry[sensor_name]:{text_format}}'
            except Exception as e:
                self.sensor_has_error.append(sensor_name)
                logging.warning(
                    f'Ошибка в параметре форматирования: {e}. ID ={id} data-sensor-name={sensor_name} data-sensor-text-format={text_format}')
                continue

        # Обновляем картинку данными сенсоров
        self.renderer.load(ET.tostring(self.svg_root))
        svg_size = self.renderer.defaultSize()
        self.scene.setSceneRect(0, 0, svg_size.width(), svg_size.height())
        self.svg_item.update()


    def __init__(self):
        super().__init__()
        # Инициализируем общие переменные
        self.sensor_has_error = []

        self.setWindowTitle(f'WT MDF {version}')

        # Инициализация графических элементов
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        # Загрузка SVG-изображения
        self.renderer = QSvgRenderer(self.file_path)
        if not self.renderer.isValid():
            raise ValueError("Ошибка загрузки SVG-файла")

        # Парсим SVG как XML
        self.svg_tree = ET.parse(self.file_path)
        self.svg_root = self.svg_tree.getroot()

        self.svg_item = QGraphicsSvgItem()
        self.svg_item.setSharedRenderer(self.renderer)
        self.scene.addItem(self.svg_item)


        # Установка размеров сцены
        svg_size = self.renderer.defaultSize()
        self.scene.setSceneRect(0, 0, svg_size.width(), svg_size.height())
        self.scene.setBackgroundBrush(Qt.black)
        # Настройка отображения
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setAlignment(Qt.AlignCenter)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Загрузка настроек
        self.load_window_settings()

        self.updateMFD({})

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

    # Приемник сообщений из нитки отвечающий за чтение данных из WT
    @QtCore.pyqtSlot(object)
    def telemetryProcessor(self, object):
        self.updateMFD(object)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
