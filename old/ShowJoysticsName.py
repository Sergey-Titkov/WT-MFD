# Подавляем сообщение:
# pygame 2.6.0 (SDL 2.28.4, Python 3.12.3)
# Hello from the pygame community. https://www.pygame.org/contribute.html
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

if __name__ == "__main__":
    pygame.init()
    print('Joystics:')
    joysticks = {}
    for i in range(0, pygame.joystick.get_count()):
        joy = pygame.joystick.Joystick(i)
        print('  ',joy.get_name())