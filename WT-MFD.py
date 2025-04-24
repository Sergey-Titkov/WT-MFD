import sys
import logging
import typing
from datetime import datetime
from sys import exception

from PyQt5 import QtCore
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtCore import Qt, QSettings, QByteArray, QObject, QThread
# import xml.etree.ElementTree as etree
from lxml import etree
from WarThunder import telemetry
import copy
import json


version = '0.0.2'


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
                current_time = datetime.now()
                full_telemetry['clock_hour'] = current_time.hour
                full_telemetry['clock_min'] = current_time.minute
                full_telemetry['clock_sec'] = current_time.second
                full_telemetry['clock_microsecond'] = current_time.microsecond
            self.telemetrySignal.emit(full_telemetry)


class MainWindow(QMainWindow):
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    file_path = "main.svg"

    def sensor_vfe_combat(self, indicator, telemetry):
        print(telemetry['VFE'])
        if 'Combat' in telemetry['Flaps position']:
            #  # Расчет наклона Только надо найти диапазон!
        #k = (y2 - y1) / (x2 - x1)
        # Вычисление Y для заданного X
        #Y = k * (X - x1) + y1
            pass
        else:
            # Надо скрыть индикатор
            # Определяем, является ли элемент tspan
            tag_local = indicator.tag.split('}')[-1]  # Локальное имя тега без namespace
            if tag_local == 'tspan':
                # Получаем родительский элемент
                parent = indicator.getparent()
                if parent is not None:
                    # Проверяем не входит ли родительский элемент в группу, если да, то скрываем всю группу
                    group = parent.getparent()
                    if group is not None and group.tag.split('}')[-1] == 'g':
                        # Скрываем всю группу
                        group.set('display', 'none')
                    else:
                        # Скрываем только родительский элемент text
                        parent.set('display', 'none')
            else:
                # Проверяем входит ли элемент в группу
                group = indicator.getparent()
                if group is not None and group.tag.split('}')[-1] == 'g':
                    # Скрываем всю группу
                    group.set('display', 'none')
                else:
                    # Скрываем сам элемент
                    indicator.set('display', 'none')

        pass

    def sensor_vlo(self, indicator, telemetry):
        """
        Возвращает критическую скорость выпуска шасси если шасси не выпущены.
        В случае если выпущены возрващает проценты до отлома шасси на земпле

        :param indicator: Куда будем помещать значение
        :param telemetry: Словарь с телеметрией от WT
        """

        gear_percent = int(telemetry['gear, %'])
        crit_gear_speed = telemetry['VLO']
        tas = telemetry['TAS, km/h']
        ias = telemetry['IAS, km/h']

        # Закрылки убраны
        value = (ias / crit_gear_speed) * 100
        text_node = int(crit_gear_speed)
        key_name = 'gear_up'

        # Шасси полностью выпущены, считаем что мы на земле
        if gear_percent==100:
            # У некоторых самолетов критическая скорость ВЫПУСКА шасси большая, например 700
            # А скорость когда шасси сломаются на земле, намного меньше, пока поставил 450
            if crit_gear_speed > 450:
                crit_gear_speed = 450
            value = (tas/crit_gear_speed)*100
            text_node = int(value)
            key_name = 'gear_down'
        else:
            # То ли убираем, то ли выпускаем
            if 0 <gear_percent<100:
                value = (ias / crit_gear_speed) * 100
                text_node = int(value)
                key_name = 'gear_down'

        indicator.text = f'{text_node}'
        # Применяем условное форматирование
        data_boundary_value = indicator.get('data-boundary-value', '').strip()
        if data_boundary_value != '':
            boundary_list = json.loads(data_boundary_value)
            if key_name in boundary_list:
                boundaries = boundary_list[key_name]
                for item in boundaries:
                    if 'boundary' in item and "style" in item:
                        if value< item['boundary']:
                            indicator.set('style', item['style'])
                            break

    def sensor_flaps_indicator(self, indicator, telemetry):
        """
        Возвращает тектовое представление того, где находятся закрылки :) и промежуточных состояний.
        Позиция: БОЙ, ВЗЛЁТ, ПОСАДКА
        В процессе смены возвращается строка вида: <Начальная позиция><---><Конечная позиция>

        :param indicator: Куда будем помещать значение
        :param telemetry: Словарь с телеметрией от WT
        """
        exact_value = []
        range_value = []
        prev_value = 1
        prev_marker = "0"
        value = int(telemetry['flaps, %'])

        exact_value.append([0, "",'up'])

        if 'Flaps position' in telemetry and 'Combat' in  telemetry['Flaps position']:
            exact_value.append([int(telemetry['Flaps position']['Combat']), "БОЙ", 'combat'])
            range_value.append([prev_value,int(telemetry['Flaps position']['Combat']),prev_marker,"Б"])
            prev_value = int(telemetry['Flaps position']['Combat'])+ 1
            prev_marker = "Б"

        if 'Flaps position' in telemetry and 'Takeoff' in  telemetry['Flaps position']:
            exact_value.append([int(telemetry['Flaps position']['Takeoff']), "ВЗЛЁТ",'takeoff'])
            range_value.append([prev_value,int(telemetry['Flaps position']['Takeoff']),prev_marker,"В"])
            prev_value = int(telemetry['Flaps position']['Takeoff']) + 1
            prev_marker = "В"

        exact_value.append([100, "ПОСАДКА",'landing'])
        range_value.append([prev_value,100,prev_marker,"П"])
        # Проверям, что попали точно в значение
        text_node = ''
        key_name = ''
        for item in exact_value:
            if value == item[0]:
                text_node = item[1]
                key_name = item[2]

        # Мы в процессе, то ли убираем, то ли выпускаем шасси
        if text_node == '':
            key_name = "process"
            # Ищем в каком мы диапазоне
            for item in range_value:
                if item[0] <= value < item[1]:
                    percent = 100 * (value - item[0]) / ((item[1] - item[0]))
                    if percent < 33:
                        text_node = fr'{item[2]}<|-->{item[3]}'
                    else:
                        if percent < 66:
                            text_node = fr'{item[2]}<-|->{item[3]}'
                        else:
                            text_node = fr'{item[2]}<--|>{item[3]}'

        indicator.text = text_node
        # Применяем условное форматирование
        data_boundary_value = indicator.get('data-boundary-value', '').strip()
        if data_boundary_value != '':
            boundary_list = json.loads(data_boundary_value)
            if key_name in boundary_list:
                indicator.set('style', boundary_list[key_name]["style"])

    def sensor_gear_indicator(self, indicator, telemetry):
        """
        Устанавливает стиль в зависимости от положения шасси, для элемента с именем: gear_indicator
        Доступны стили для положения:
        - Шасси выпущены("down")
        - В процессе("process")
        - Шасси убраны("up")
        Пример:
            data-boundary-value='{
                                    "down":   {"style": "fill: rgb(255, 86, 48); font-size: 60px; font-family: Consolas; font-weight: 550"},
                                    "process":{"style": "fill: rgb(0, 157, 2)  ; font-size: 60px; font-family: Consolas; font-weight: 550"},
                                    "up":     {"style": "visibility: hidden"}
                                 }'
            В случае если шасси убраны индикатор полностью скрывается
        :param indicator: Куда будем помещать значение
        :param telemetry: Словарь с телеметрией от WT
        """

        value = int(telemetry['gear, %'])
        key = 'down'
        if 0 < value < 100:
            key = 'process'
        else:
            if value ==0:
                key = 'up'

        # Применяем условное форматирование
        data_boundary_value = indicator.get('data-boundary-value', '').strip()
        if data_boundary_value != '':
            boundary_list = json.loads(data_boundary_value)
            if key in boundary_list:
                indicator.set('style', boundary_list[key]["style"])

    def sensor_altitude_u(self, indicator, telemetry):
        """
        Устанавливает значение для сенсора: altitude_u
        Алгорим следующий, если есть радио высота то устанавливаем ее, если ее нет то барометрическую, для барометрической высоты добавляем 🛆 перед числом

        :param indicator: Куда будем помещать значение
        :param telemetry: Словарь с телеметрией от WT
        """
        # Рассчитываем значение
        text_format = indicator.get('data-sensor-text-format', '').strip()
        value = float(telemetry['altitude_hour'])
        indicator.text = f'🛆{value:{text_format}}'
        if 'radio_altitude_m' in telemetry:
            value = float(telemetry['radio_altitude_m'])
            indicator.text = f'{value:{text_format}}'

        # Применяем условное форматирование
        data_boundary_value = indicator.get('data-boundary-value', '').strip()
        if data_boundary_value != '':
            boundary_list = json.loads(data_boundary_value)
            for item in boundary_list:
                if value < float(item["boundary"]):
                    indicator.set('style', item["style"])
                    break

    def update_mfd(self, telemetry):

        if not telemetry:
            self.svg_item.setVisible(False)
            return
        else:
            if not self.svg_item.isVisible():
                self.svg_item.setVisible(True)

        # Работать будем с копией изначальной картинки, иначе задолбаешься потом находить и показывать все скрытые элементы.
        svg_work_copy = copy.deepcopy(self.svg_root)
        # Находим все элементы с атрибутом data-sensor-name во всем дереве
        elements = svg_work_copy.findall('.//*[@data-sensor-name]', namespaces=self.namespaces)
        for indicator in elements:
            # Безопасно получаем атрибуты
            id = indicator.get('id', '').strip()
            sensor_name = indicator.get('data-sensor-name', '').strip()
            text_format = indicator.get('data-sensor-text-format', '').strip()
            data_boundary_value = indicator.get('data-boundary-value', '').strip()

            # Имя сенсора должно быть задано
            if not sensor_name:
                continue
            # Обрабатываем только сенсоры у которых не было ошибок
            if sensor_name in self.sensor_has_error:
                continue
            # Обрабатываем индикаторы
            try:
                if sensor_name in ['altitude_u', 'gear_indicator', 'flaps_indicator', 'VLO', 'VFE_Combat']:
                    match sensor_name:
                        case 'altitude_u':
                            self.sensor_altitude_u(indicator, telemetry)
                        case 'gear_indicator':
                            self.sensor_gear_indicator(indicator, telemetry)
                        case 'flaps_indicator':
                            self.sensor_flaps_indicator(indicator, telemetry)
                        case 'VLO':
                            self.sensor_vlo(indicator, telemetry)
                        case 'VFE_Combat':
                            self.sensor_vfe_combat(indicator, telemetry)
                        case _:
                            pass
                    continue

            except Exception as e:
                self.sensor_has_error.append(sensor_name)
                logging.error(f'Возникла ошибка: {e}. ID ={id} data-sensor-name={sensor_name} sensor_value={telemetry[sensor_name]}')
                continue

            # Если сенсора не нашли в телеметрии, то скрываем его
            if sensor_name not in telemetry:
                # Определяем, является ли элемент tspan
                tag_local = indicator.tag.split('}')[-1]  # Локальное имя тега без namespace
                if tag_local == 'tspan':
                    # Получаем родительский элемент
                    parent = indicator.getparent()
                    if parent is not None:
                        # Проверяем не входит ли родительский элемент в группу, если да, то скрываем всю группу
                        group = parent.getparent()
                        if group is not None and group.tag.split('}')[-1] == 'g':
                            # Скрываем всю группу
                            group.set('display', 'none')
                        else:
                            # Скрываем только родительский элемент text
                            parent.set('display', 'none')
                else:
                    # Проверяем входит ли элемент в группу
                    group = indicator.getparent()
                    if group is not None and group.tag.split('}')[-1] == 'g':
                        # Скрываем всю группу
                        group.set('display', 'none')
                    else:
                        # Скрываем сам элемент
                        indicator.set('display', 'none')
                continue
            # Устанавливаем значение сенсора
            try:
                indicator.text = f'{telemetry[sensor_name]:{text_format}}'
            except Exception as e:
                self.sensor_has_error.append(sensor_name)
                logging.warning(
                    f'Ошибка в параметре форматирования: {e}. ID ={id} data-sensor-name={sensor_name} data-sensor-text-format={text_format}')
                continue

            # Применяем условное форматирование
            try:
                if data_boundary_value != '':
                    value = float(telemetry[sensor_name])
                    boundary_list = json.loads(data_boundary_value)
                    for item in boundary_list:
                        if value < float(item["boundary"]):
                            indicator.set('style', item["style"])
                            break
            except Exception as e:
                self.sensor_has_error.append(sensor_name)
                logging.warning(
                    f'Ошибка в условном форматировании форматирования: {e}. ID ={id} data-sensor-name={sensor_name} data-sensor-text-format={text_format}  data_boundary_value={data_boundary_value} sensor_value={telemetry[sensor_name]} ')
                continue

        # Обновляем картинку данными сенсоров
        self.renderer.load(etree.tostring(svg_work_copy))
        svg_size = self.renderer.defaultSize()
        self.scene.setSceneRect(0, 0, svg_size.width(), svg_size.height())
        self.svg_item.update()

    def __init__(self):
        super().__init__()

        self.fm_data = {}

        try:
            # Загружаем данные полученные из флайт модели
            with open('wtmfd_data.json', 'r', encoding="utf-8") as file:
                self.fm_data.update(json.load(file))
        except Exception as e:
            logging.warning(f'При загрузке данных из флайт модели возникла ошибка: {e} ')

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
        self.svg_tree = etree.parse(self.file_path)
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

        self.update_mfd({})

        # Обрабатываем телеметрию
        # Создаем нить
        self.threadWT = QThread()
        # Создаем обработчик
        self.browserWT = BrowserWT()
        # Перемещаем обработчик в нить
        self.browserWT.moveToThread(self.threadWT)
        # Связываем обработчики сигналов
        self.browserWT.telemetrySignal.connect(self.telemetry_processor)
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
    def telemetry_processor(self, object):
        # Обогащаем данные телеметрии данными из флайт модели и данными полученными на основании расчетов
        telem = None
        if object is not None:
            telem = object.copy()
            if 'radio_altitude' in telem:
                # Вычислям радио высоту в метрах
                telem['radio_altitude_m'] = float(telem['radio_altitude']) * 0.3048

            if 'type' in telem:
                plane_id = telem['type']
                if plane_id in self.fm_data:
                    telem['VNE'] = self.fm_data[plane_id]['VNE']
                    telem['MNE'] = self.fm_data[plane_id]['MNE']
                    telem['Name'] = self.fm_data[plane_id]['Name']['English']
                    telem['Length'] = self.fm_data[plane_id]['Length']
                    telem['WingSpan'] = self.fm_data[plane_id]['WingSpan']
                    telem['WingArea'] = self.fm_data[plane_id]['WingArea']
                    telem['EmptyMass'] = self.fm_data[plane_id]['EmptyMass']
                    telem['MaxFuelMass'] = self.fm_data[plane_id]['MaxFuelMass']
                    telem['VLO'] = self.fm_data[plane_id]['VLO']
                    telem['Flaps position'] = self.fm_data[plane_id]['Flaps']
                    telem['VFE'] = self.fm_data[plane_id]['VFE']
                    telem['CritWingOverload'] = self.fm_data[plane_id]['CritWingOverload']
                    telem['NumEngines'] = self.fm_data[plane_id]['NumEngines']
                    telem['RPMMin'] = self.fm_data[plane_id]['RPM']['RPMMin']
                    telem['RPMMax'] = self.fm_data[plane_id]['RPM']['RPMMax']
                    telem['RPMMaxAllowed'] = self.fm_data[plane_id]['RPM']['RPMMaxAllowed']
                    telem['MaxNitro'] = self.fm_data[plane_id]['MaxNitro']
                    telem['NitroConsum'] = self.fm_data[plane_id]['NitroConsum']
                    telem['CritAoA'] = self.fm_data[plane_id]['CritAoA']

        self.add_vne_persent(telem)
        self.update_mfd(telem)

    def add_vne_persent(self, telem):
        """ Добавляем в телеметрию параметр VNE % - процент от критической скорости
        Алгоритм расчета, считаем:
          - IAS, km/h / VNE
          - M / MNE
        Какое значение больше то и добавляем в телеметрию
        :param telem: Словарь с данными телемерии
        :return:
        """
        try:
            if telem is not None and 'VNE' in telem and 'MNE' in telem:
                vne_percent = telem['IAS, km/h'] / telem['VNE'][0][1]
                mne_percent = telem['M'] / telem['MNE'][0][1]
                result_percent = mne_percent
                if vne_percent > mne_percent:
                    result_percent = vne_percent
                telem['VNE %'] = f'{float(result_percent * 100):.0f}'
        except Exception as e:
            logging.warning(f'{e} ')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
