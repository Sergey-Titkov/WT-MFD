import sys
import logging
from datetime import datetime
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtCore import Qt, QSettings, QByteArray, QObject, QThread

import xml.etree.ElementTree as ET

# Класс для получения телеметрии из WT
class BrowserWT(QObject):
    #telem = telemetry.TelemInterface()
    telemetrySignal = QtCore.pyqtSignal(object)
    def run(self):
        while True:
            QtCore.QThread.msleep(100)
            telemetry = {'valid': True, 'army': 'air', 'type': 'su_30sm', 'speed': 0.032378, 'pedals': 0.0,
                         'pedals1': 0.0,
                         'pedals2': 0.0, 'pedals3': 0.0, 'pedals4': 0.0, 'pedals5': 0.0, 'pedals6': 0.0, 'pedals7': 0.0,
                         'pedals8': 0.0, 'stick_elevator': -0.011281, 'stick_ailerons': 0.0, 'vario': 0.007959,
                         'altitude_hour': 36.322304, 'altitude_min': 36.322304, 'altitude_10k': 36.322304,
                         'altitude1_hour': 36.322304, 'altitude1_10k': 36.322304, 'aviahorizon_roll': 0.058864,
                         'aviahorizon_pitch': 0.021007, 'bank': 0.058864, 'compass': 270.918518, 'compass1': 270.918518,
                         'clock_hour': 0.85, 'clock_min': 51.0, 'clock_sec': 19.0, 'rpm': 5067.244629,
                         'rpm1': 5065.077637,
                         'airbrake_lever': 0.0, 'gears': 0.5, 'gear_lamp_down': 1.0, 'gear_lamp_up': 1.0,
                         'gear_lamp_off': 1.0, 'throttle': 0.0, 'throttle1': 0.0, 'weapon2': 0.0, 'g_meter': 1.000369,
                         'g_meter_min': 0.942094, 'g_meter_max': 1.074686, 'aoa': -13.788331, 'blister1': 1.0,
                         'blister2': 1.0, 'blister3': 1.0, 'blister4': 1.0, 'blister5': 1.0, 'blister6': 1.0,
                         'blister11': 1.0, 'alt_m': 11.071038259200002, 'aileron, %': 0, 'elevator, %': -1,
                         'rudder, %': 0,
                         'flaps, %': 0, 'gear, %': 100, 'airbrake, %': 0, 'H, m': 36, 'TAS, km/h': 0, 'IAS, km/h': 0,
                         'M': 0.0, 'AoA, deg': -13.6, 'AoS, deg': -10.1, 'Ny': 0.94, 'Vy, m/s': 0.0, 'Wx, deg/s': 0,
                         'Mfuel, kg': 9400, 'Mfuel0, kg': 9400, 'throttle 1, %': 0, 'power 1, hp': 0.0, 'RPM 1': 5065,
                         'manifold pressure 1, atm': 1.0, 'oil temp 1, C': 65, 'thrust 1, kgs': 359,
                         'efficiency 1, %': 0,
                         'throttle 2, %': 0, 'power 2, hp': 0.0, 'RPM 2': 5068, 'manifold pressure 2, atm': 1.0,
                         'oil temp 2, C': 65, 'thrust 2, kgs': 359, 'efficiency 2, %': 0, 'lat': -0.2853561339909174,
                         'lon': 0.3980051562695432}
            current_time=datetime.now()
            telemetry['clock_hour'] = current_time.hour
            telemetry['clock_min'] = current_time.minute
            telemetry['clock_sec'] = current_time.second
            telemetry['clock_microsecond'] = current_time.microsecond

            # Пока без событий и чата
            #result = None
            #if self.telem.get_telemetry(comments=False, events=False):
            #    result = self.telem
            #    print('BrowserWT')
            # Через сигнал обновляем экранную форму.
            self.telemetrySignal.emit(telemetry)

class MainWindow(QMainWindow):
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    file_path = "MFD - 01___.svg"

    def updateMFD(self,telemetry):

        if not telemetry:
            self.svg_item.setVisible(False)
            return

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
                self.sensor_has_error.append(sensor_name)
                logging.warning(f'Параметр не найден: ID ={id} data-sensor-name={sensor_name}')
                continue
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
        self.svg_item.setVisible(False)
        self.svg_item.setVisible(True)


    def __init__(self):
        super().__init__()
        # Инициализируем общие переменные
        self.sensor_has_error = []

        self.setWindowTitle("SVG Viewer")

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
