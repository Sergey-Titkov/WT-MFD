# Подавляем сообщение:
# pygame 2.6.0 (SDL 2.28.4, Python 3.12.3)
# Hello from the pygame community. https://www.pygame.org/contribute.html
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import keyboard
import pygame
import types
import time
from datetime import datetime
import json

#32

if __name__ == "__main__":
    start_time = time.time()
    bind = types.SimpleNamespace()
    bind.eventOccur = False
    bind.keys=[["S-TECS MODERN THROTTLE MAX STEM", 32, 0]]

    with open('WriteTimeOffsetToFile.cfg') as f:
        templates = json.load(f)

    bind.keys = []
    for key in templates:
        bind.keys.append([key[0], key[1], 0])

    print(bind.keys)

    pygame.init()
    joysticks = {}
    joysticksState = {}

    for i in range(0, pygame.joystick.get_count()):
        joy = pygame.joystick.Joystick(i)
        joy.init()
        joysticks[joy.get_instance_id()] = joy
        joysticksState[joy.get_instance_id()] = [0] * 128
        print(joy.get_instance_id(), ' - ', joysticks[joy.get_instance_id()].get_name())

    while True:

        for event in pygame.event.get():
            joyAction = (event.type == pygame.JOYBUTTONDOWN) or (event.type == pygame.JOYBUTTONUP)
            if event.type == pygame.JOYBUTTONDOWN:
                joysticksState[event.instance_id][event.button] = 1

            if event.type == pygame.JOYBUTTONUP:
                joysticksState[event.instance_id][event.button] = 0

            if joyAction:
                for bindKey in bind.keys:
                    for ind in joysticks:
                        if bindKey[0] == joysticks[ind].get_name():
                            bindKey[2] = joysticksState[ind][bindKey[1]]
                action = True
                for bindKey in bind.keys:
                    action = action and bindKey[2] == 1

                if not bind.eventOccur and action:
                    line = f"{int(time.time() - start_time)}\t{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
                    print(line)
                    with open('WriteTimeOffsetToFile.log', 'a') as f:
                        f.write(line+'\n')

                    bind.eventOccur = action

                if bind.eventOccur and not action:
                    bind.eventOccur = False


#                print(joysticks[event.instance_id].get_name(),' ',joysticksState[event.instance_id])

        if keyboard.is_pressed('q'):
            print("Завершаем работу.")
            break
