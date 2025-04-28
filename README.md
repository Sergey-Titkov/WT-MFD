# Зачем
Программа предназначена для вывода окна с телеметрией War Thunder на отдельный дисплей.
Это попытка повторения настоящего MFD :) 
Выглядит это вот так:

![2025-04-28 11-01-56](https://github.com/user-attachments/assets/5bfbca55-43fb-47d8-b3cd-46342c9ab05f)

# Установка 
## Из исходников
Вам хочется получить всё от возможностей программ с открытым кодом, похвально! Итак, скачиваем python: https://www.python.org/downloads/release/python-3129/
Да вот этот конкретный релиз, потому что программа разработана на нём. Устанавливаем, и не забываем поставить галочку: добавить в системные переменные.
Открываем консоль(Пуск => cmd) и вводим команду: ```python --version```
Должно быть так:
```cmd
C:\Users\user>python --version
Python 3.12.9

C:\Users\user>
```
Дальше, качаем архив с исходными кодами:

![image](https://github.com/user-attachments/assets/9080454a-dd5e-429e-a79d-aaafa60ff2b9)

Разархивируем куда надо и получаем:

![image](https://github.com/user-attachments/assets/11d9736f-d964-448e-bced-d9cf2a5363ce)

Теперь надо настроить окружение. Запускаем: init.bat 
После чего можно запускать программу: run.bat
Перетаскиваем окно на ваш mfd :) и максимизируем.
Все можно запускать War Thunder и вылетать.
Пока не запущен War Thunder экран будет черный.

## Исполняемый файл
### Важно
Я создал исполняемые файлы с помощью команды pyinstaller --onefile wt-mfd.py 
В результате проверки на virustotal имеем следующее:

![image](https://github.com/user-attachments/assets/8f94aa7e-570d-4595-8278-12ad8cd3d2a0)

Я попробовал нутику, результаты то же фиговые, кто знает подскажите в коментах как бороться

Скачиваем дистрибутив: 

![image](https://github.com/user-attachments/assets/29123152-20f2-4a1d-bb40-a4ca98446870)

Распаковываем и запускаем.

# Настройка отображения индикаторов
## Важно
То что вы видете на экране это файл main.svg где значения параметров телеметрии подставляются в текстовые поля. Для svg поддерживается только урезанный стандарт: https://www.w3.org/TR/SVGTiny12/ - имейте ввиду.
Вы можете добавлять любые элементы и изменять текущие под свои нужды. Если не знакомы с svg рекомендую посмотреть видео. Можно использовать специальные редакторы для редактирования, но с оговоркой, редакторы используют полную спецификацию svg и ряд вещей не будет отображаться правильно.
Я использую встроенный в pyCharm редактор, я меню код svg, а редактор отображает измения.

![image](https://github.com/user-attachments/assets/d0fc539d-a31c-4984-9849-87b05877b0c6)

Для меня это самый удобный вариант.

## С чего начать
Установить размер svg под разрешение ВАШЕГО MFD
Вторая строка в файле: ```<svg width="1024" height="576" version="1.1" id="svg1" xmlns="http://www.w3.org/2000/svg">```
Устанавливаем ширину: width и высоту: height. Но с высотой естью нюанс, она должна быть на 24 пикселя меньше чем выстота экрана, потому что на экране есть строка сверух.
У меня разрешение экрана 1024 на 600 поэтому значения 1024 на 576.
Теперь можно добавлять любой индикатор из списка ниже.

## Добавление индикатора
Допустим вы хотите добавить на истинную скорость на MFD.
Нет ничего проще, открываем в любом текстовом редакторе main.svg и добавляем строку
```xml
  <text x="70" y="178" style="fill: rgb(0, 157, 2); font-family: Arial, sans-serif; font-size: 20px; font-weight: 700; white-space: pre;"
       data-sensor-name="TAS, km/h"
       data-sensor-text-format="1.2f"
       >9.99</text>
```
Сохраняем, запускаем, заходим в бой и видим:

![image](https://github.com/user-attachments/assets/97471a37-6a49-439b-ab61-1c3bdbb6381d)

На земле скорость понятно будет 0.00. Текст заменился на значение идикатора: ```data-sensor-name="TAS, km/h"```, а форматирование произошло по формату: ```data-sensor-text-format="1.2f"```, что означает два знака после запятой. Не нужна дробная часть: ```data-sensor-text-format=".0f"```
Как настраивать стиль, рекомендую посмотреть в документации.
Возникает вопрос, а где же название? Ответ все в ручную. Добавляем название сенсора перед значением сенсора и наш код становиться вот таким:
```xml
  <text style="fill: rgb(0, 157, 2); font-family: Arial, sans-serif; font-size: 20px; font-weight: 700; white-space: pre;" x="25" y="178">TAS</text>
  <text style="fill: rgb(0, 157, 2); font-family: Arial, sans-serif; font-size: 20px; font-weight: 700; white-space: pre;" x="70" y="178" data-sensor-name="TAS, km/h" data-sensor-text-format="1.2f">9.99</text>
```

Заходим в воздушный бой и видм:

![image](https://github.com/user-attachments/assets/74ca1c09-d9dd-48f9-9bbf-e2c1d0516510)

То что и хотелось! 
В атрибут: ```data-sensor-name``` помещаем имя сенсора из списка ниже, в ```data-sensor-text-format``` формат в котором хотите его увидеть. В данном случае это число с фиксировнным количеством знаков после точки. 
Если не знаете что писать просто не создавайте или не заполняйте атрибут, тогда значения будут представлены как есть.
Если хочется шикануть, то вполне можно использовать tspan, пример показан ниже.
```xml
   <text x="25" y="150" font-size="30" style="fill: rgb(0, 157, 2); font-size: 20px; font-family: Arial">
    <tspan text-anchor="start" style="font-weight: 550" >IAS:</tspan>
    <tspan data-sensor-name="IAS, km/h" text-anchor="start" dx="0" style="font-weight: 700">1135.00</tspan>
    <tspan text-anchor="start" dx="5" style="fill: rgb(38, 153, 38); font-size: 19px">км/ч</tspan>
  </text>
```
![image](https://github.com/user-attachments/assets/f5d2d5b8-be3b-4bd2-876f-be3019dc07ce)

## Скрытие сенсора
Если имени сенсора из ```data-sensor-name``` нет в списке телеметрии, то в этом случае элемент содрежащий этот сенсор скрывается. Причем если имя сенсора находится в tspan то будет скрыт родительский элемент text. Если же элемент text находится в группе то будет скрыта вся группа. Это может потребоваться например для скрытия данных по второму двигателю для одномоторных самолетов.
Ниже представлен пример реалзиующий эту логику. Параметры каждого двигателя помещены в отдельную группу и в случае если данных по нему нет то они будут скрыты.
```xml
<!-- параметры первого двигателя -->
<g style="fill: rgb(0, 157, 2); font-size: 20px; font-family: Consolas">
    <!-- Мощность первого двигателя -->
    <text x="850" y="477">МОЩ</text>
    <text x="970" y="477" style="font-weight: 700" text-anchor="end" data-sensor-name="thrust 1, kgs" data-sensor-text-format=".0f">9</text>
    <text x="975" y="477">кгс</text>

    <!-- Обороты первого двигателя -->
    <text x="850" y="500">ОБ</text>
    <text x="970" y="500" style="font-weight: 700" text-anchor="end" data-sensor-name="RPM 1" data-sensor-text-format=".0f">9</text>
</g>

<!-- параметры второго двигателя -->
<g style="fill: rgb(0, 157, 2); font-size: 20px; font-family: Consolas">
    <!-- Мощность второго двигателя -->
    <text x="850" y="530">МОЩ</text>
    <text x="970" y="530" style="font-weight: 700" text-anchor="end" data-sensor-name="thrust 2, kgs" data-sensor-text-format=".0f">9</text>
    <text x="975" y="530">кгс</text>

    <!-- Обороты второго двигателя -->
    <text x="850" y="553">ОБ</text>
    <text x="970" y="553" style="font-weight: 700" text-anchor="end" data-sensor-name="RPM 2" data-sensor-text-format=".0f">9</text>
</g>
```
Как это выглдяить.
Для одномоторного самолета:
![image](https://github.com/user-attachments/assets/450a6c0a-f181-42c6-a36c-0350033ee11a)

Для двух моторного самолета:
![image](https://github.com/user-attachments/assets/57e30d04-addb-4831-ab16-a83b6e896d95)


## Условное форматирование
Для каждого сенсора можно задать условное форматирование. То есть вид значения в зависимости от его значения. Реализуется через атрибут ```data-boundary-value```
Рассмотрим на примере для критической скорости самолета в процентах.
Код для сенсора имеет вид:
```xml
<!-- Критическая скорость в процентах -->
<g style="fill: rgb(67, 230, 103); font-size: 55px; font-family: Consolas">
    <text x="260" y="303" style="font-weight: 550">КС</text>
    <text x="707" y="303" text-anchor="end"
          data-sensor-name="VNE %"
          data-boundary-value='
                                [
                                    {"boundary": 80, "style": "fill: rgb(67, 230, 103)"},
                                    {"boundary": 90, "style": "fill: rgb(255, 232, 0)"},
                                    {"boundary": 95, "style": "fill: rgb(255, 0, 0)"},
                                    {"boundary": 120, "style": "fill: rgb(148, 4, 4)"}
                                ]
                            '>
        120
    </text>
    <text x="735" y="303" style="fill: rgb(0, 157, 2)">%</text>
</g>
```
Если значение сенсора находится в границах от 0 по 80 то индикатор будет зеленым, от 81 по 90 - желтым, от 91 по 95 - ярко красным и в финале очень темно красным. Стиль понятное дело может быть любым. 
Собственно значение атрибута style копируется в атрибут style текста.

# Список доступных сенсоров
 - aileron, %":2,
 - airbrake, %":0,
 - airbrake_lever":0.0,
 - alt_m":68.452589028,
 - altitude1_10k":224.581985,
 - altitude1_hour":224.581985,
 - altitude_10k":224.581985,
 - altitude_hour":224.581985,
 - altitude_min":224.581985,

## altitude_u
Универсальная высота. 
Если есть радио высота то будет возращена она, если ее нет то будет использована барометрическая высота. 
Для барометрической высоты будет добавлен знак: 🛆 перед числом. На условное форматирование знак не влияет и не участвует в нем.

 - aoa":5.05461,
 - AoA, deg":5.0,
 - AoS, deg":-0.5,
 - army":"air",
 - aviahorizon_pitch":22.053192,
 - aviahorizon_roll":-1.948857,
 - bank":0.622094,
 - blister1":0.0,
 - blister11":0.0,
 - blister2":0.0,
 - blister3":0.0,
 - blister4":0.0,
 - blister5":0.0,
 - blister6":0.0,
 - clock_hour":22,
 - clock_microsecond":264759,
 - clock_min":18,
 - clock_sec":11,
 - compass":264.01004,
 - compass1":264.01004,
 - CritAoA":[      [         0,         32.0,         -20.0,         30.0,         -22.0      ]   ],
 - CritWingOverload":[      [         0,         -530000.0,         1600000.0      ]   ],
 - efficiency 1, %":0,
 - efficiency 2, %":0,
 - elevator, %":-9,
 - EmptyMass":18830,
 - Flaps position":{      "Takeoff":90.0   },
 - flaps, %":53,

## flaps_indicator
Возвращает тектовое представление того, где находятся закрылки :) и промежуточных состояний.
Позиция: БОЙ, ВЗЛЁТ, ПОСАДКА
В процессе смены возвращается строка вида: <Начальная позиция><---><Конечная позиция>
Доступны стили для положения:
 - Убраны("up")
 - В процессе("process")
 - БОЙ("combat")
 - ВЗЛЁТ("takeoff")
 - ПОСАДКА("landing")
Пример:
```
        data-boundary-value='{
                                "up":      {"style": "visibility: hidden"},
                                "process": {"style": "fill: #FFAB00; font-size: 60px; font-family: Consolas; font-weight: 550"},
                                "combat":  {"style": "fill: #36B37E; font-size: 60px; font-family: Consolas; font-weight: 550"},
                                "takeoff": {"style": "fill: #36B37E; font-size: 60px; font-family: Consolas; font-weight: 550"},
                                "landing": {"style": "fill: #36B37E; font-size: 60px; font-family: Consolas; font-weight: 550"}
                            }'
```

 - g_meter":1.072995,
 - g_meter_max":1.609988,
 - g_meter_min":0.778297,
 - gear, %":0,

## gear_indicator
Тестовый индикатор шасси.
Значение не возращает, только меняет стиль в зависимости от положения шасси.
Доступны стили для положения:
 - Шасси выпущены("down")
 - В процессе("process")
 - Шасси убраны("up")
Пример:
```
       data-boundary-value='{
                                    "down":   {"style": "fill: rgb(255, 86, 48); font-size: 60px; font-family: Consolas; font-weight: 550"},
                                    "process":{"style": "fill: rgb(0, 157, 2)  ; font-size: 60px; font-family: Consolas; font-weight: 550"},
                                    "up":     {"style": "visibility: hidden"}
                                 }'
```
В случае если шасси убраны индикатор полностью скрывается

 - gear_lamp_down":0.0,
 - gear_lamp_off":0.0,
 - gear_lamp_up":0.0,
 - gears":0.5,
 - H, m":231,
 - IAS, km/h":393,
 - lat":-0.2860662101410436,
 - Length":21.93,
 - lon":0.3933537473068663,
 - M":0.32,
 - manifold pressure 1, atm":1.0,
 - manifold pressure 2, atm":1.0,
 - MaxFuelMass":9400.0,
 - MaxNitro":0.0,
 - Mfuel, kg":9400,
 - Mfuel0, kg":9400,
 - MNE":[      [         0,         2.1      ]   ],
 - Name":"Su-30SM",
 - NitroConsum":0.0,
 - NumEngines":2,
 - Ny":1.03,
 - oil temp 1, C":94,
 - oil temp 2, C":94,
 - pedals":-0.045684,
 - pedals1":-0.045684,
 - pedals2":-0.045684,
 - pedals3":-0.045684,
 - pedals4":-0.045684,
 - pedals5":-0.045684,
 - pedals6":-0.045684,
 - pedals7":-0.045684,
 - pedals8":-0.045684,
 - power 1, hp":0.0,
 - power 2, hp":0.0,
 - RPM 1":8350,
 - RPM 2":8350,
 - rpm":8350.0,
 - rpm1":8350.0,
 - RPMMax":8350,
 - RPMMaxAllowed":8950,
 - RPMMin":5500,
 - rudder, %":-4,
 - speed":108.382866,
 - stick_ailerons":0.018247,
 - stick_elevator":-0.097333,
 - TAS, km/h":398,
 - throttle 1, %":110,
 - throttle 2, %":110,
 - throttle":1.1,
 - throttle1":1.1,
 - thrust 1, kgs":11255,
 - thrust 2, kgs":11285,
 - type":"su_30sm",
 - valid":true,
 - vario":32.206203,
 - VFE":[      [         0.2,         1018.0      ],      [         1.0,         600.0      ]   ],
## VFE_Combat, VFE_Takeoff, VFE_Landing
Критическая скорость повреждения закрылок для каждого положения.
Если закрылки выпущены, то процент текущей скорости по IAS к критической скорости поломки закрыли в этом(БОЙ, ВЗЛЕТ, ПОСАДКА) положении для данной модели самолета.
Если закрылки убраны, то критическая скорость поломки закрылоу в этом(БОЙ, ВЗЛЕТ, ПОСАДКА) положении для данной модели самолета.
Параметры условного форматиравания разделены на две группы, когда закрылки убраны и когда закрылки выпущены.
В каждой группе можно определить свой набор значений:
```
                  data-boundary-value='{
                                          "flaps_up":  [
                                                            {"boundary": 100,   "style": "fill: #42E466"},
                                                            {"boundary": 110,   "style": "fill: #FFAB00"},
                                                            {"boundary": 1000,  "style": "fill: #FF5630"}
                                                       ],
                                          "flaps_down":  [
                                                            {"boundary": 70,   "style": "fill: #42E466"},
                                                            {"boundary": 80,   "style": "fill: #FFAB00"},
                                                            {"boundary": 1000, "style": "fill: #FF5630; font-weight:bold"}
                                                        ]
                            }'

```
## VLO
Критическая скорость повреждения шасси. 
Если шасси ПОЛНОСТЬЮ выпущены то возвращает процет текущей скорости TAS от 450 км/ч.
У большинства самолетов на 450 при взлете шассси ломаются.
Если шасси не полностью выпущены, то возвращается процет от текущй скорости IAS от критической скорости выпуска шасси для данной модели самолета.
Если шасси убраны то возвращается критической скорости выпуска шасси для данной модели самолета. 
Параметры условного форматиравания разделены на две группы, когда шасси убраны и когда шасси выпущено.
В каждой группе можно определить свой набор значений:
```
            data-boundary-value='{
                                "gear_up":  [
                                                {"boundary": 100,   "style": "fill: #42E466"},
                                                {"boundary": 110,   "style": "fill: #FFAB00"},
                                                {"boundary": 1000,  "style": "fill: #FF5630"}
                                ],
                                "gear_down":  [
                                                {"boundary": 70,   "style": "fill: #42E466"},
                                                {"boundary": 80,   "style": "fill: #FFAB00"},
                                                {"boundary": 1000, "style": "fill: #FF5630"}
                                ]
                            }'

```

## VNE %
Процент от критической скорости самолета.
Алгоритм расчета, считаем:
- "IAS, km/h"/"VNE"
- "M" / "MNE"
Какое значение больше то будет использовано

 - VNE":[      [         0,         1540      ]   ],
 - Vy, m/s":32.5,
 - weapon2":0.0,
 - WingSpan":[      [         0,         14.7      ]   ],   "WingArea":[      [         0,         61.98      ]   ],
 - Wx, deg/s":1,
