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
Дальше, качаем архив с исходными кодами
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



# Ограничения
Поддерживается только стандарт svg: https://www.w3.org/TR/SVGTiny12/

# Как использовать
## Список доступных сенсоров
- army
- type
- pedals
- pedals1
- pedals2
- pedals3
- pedals4
- pedals5
- stick_elevator
- stick_ailerons
- vario
- altitude_hour
- altitude_min
- altitude_10k
- altitude1_hour
- altitude1_min
- altitude1_10k
- aviahorizon_roll
- aviahorizon_pitch
- aviahorizon_roll1
- aviahorizon_pitch1
- bank
- compass
- compass1
- compass2
- clock_hour
- clock_min
- clock_sec
- rpm_min
- rpm_hour
- water_temperature
- fuel
- fuel1
- airbrake_lever
- gears
- gear_lamp_down
- gear_lamp_up
- gear_lamp_off
- flaps
- flaps1
- trimmer
- throttle
- weapon2
- weapon4
- flaps_indicator
- flaps_indicator1
- mach
- mach1
- g_meter
- g_meter_min
- g_meter_max
- aoa
- blister1
- blister2
- blister3
- blister4
- blister5
- blister11
- alt_m
- aileron, %
- elevator, %
- rudder, %
- flaps, %
- gear, %
- airbrake, %
- H, m
- TAS, km/h
- IAS, km/h
- M
- AoA, deg
- AoS, deg
- Ny
- Vy, m/s
- Wx, deg/s
- Mfuel, kg
- Mfuel0, kg
- throttle 1, %
- power 1, hp
- RPM 1
- manifold pressure 1, atm
- oil temp 1, C
- thrust 1, kgs
- efficiency 1, %
- lat
- lon
- clock_microsecond

## Настройка отображения
Выше представлен список доступных сенсоров, вы хотите добавить истинную скорость на MFD.
Нет ничего проще, открываем в любом текстовом редакторе main.svg и добавляем две строки
```xml
  <text style="fill: rgb(0, 157, 2); font-family: Arial, sans-serif; font-size: 20px; font-weight: 700; white-space: pre;" x="25" y="178">TAS</text>
  <text style="fill: rgb(0, 157, 2); font-family: Arial, sans-serif; font-size: 20px; font-weight: 700; white-space: pre;" x="70" y="178" id="sens_stext09" data-sensor-name="TAS, km/h" data-sensor-text-format="1.2f">9.99</text>
```
Сохранив файл и зайдя в воздушный бой в War Thunder вы увидет вот такую картинку
![image](https://github.com/user-attachments/assets/ab2e1db3-1dbb-41bd-aebe-f9cb095fbd99)
Скорость у вас будет ваша, на земле она будет 0 в воздухе, как дело пойдет.
Разберем что делают строки
```xml
  <text style="fill: rgb(0, 157, 2); font-family: Arial, sans-serif; font-size: 20px; font-weight: 700; white-space: pre;" x="25" y="178">TAS</text>
```
Она просто выводит надпись. Рекомендую посмотреть или почитать базовый вещи про svg. Там ничего сложного нет.
![image](https://github.com/user-attachments/assets/bc3082dc-814d-4ee6-b2a6-8cb40711c037)
Разбираем как получить значение сенсора.
```xml
  <text style="fill: rgb(0, 157, 2); font-family: Arial, sans-serif; font-size: 20px; font-weight: 700; white-space: pre;" x="70" y="178" id="sens_stext09" data-sensor-name="TAS, km/h" data-sensor-text-format="1.2f">9.99</text>
```
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




