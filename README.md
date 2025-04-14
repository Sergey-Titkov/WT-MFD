# WT-MFD
## Зачем
Программа предназначена для вывода окна с телеметрией War Thunder на отдельный дисплей.
Это попытка повторения настоящего MFD :)
Выглядит это вот так:
![2025-04-14 22-59-15](https://github.com/user-attachments/assets/ae362a21-4993-4149-9c3e-10a4ca9d3251)
Число в вверху это компас
Программа имет сверх гибкую настройку, так что не удивляйтесь, вас предупредели.

## Важно
Я создал исполняемые файлы с помощью команды pyinstaller --onefile wt-mfd.py 
В результате проверки на virustotal имеем следующее:
![image](https://github.com/user-attachments/assets/8f94aa7e-570d-4595-8278-12ad8cd3d2a0)
Я попробовал нутику, результаты то же фиговые, кто знает подскажите в коментах как бороться

## Как использовать
### Список доступных сенсоров
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




