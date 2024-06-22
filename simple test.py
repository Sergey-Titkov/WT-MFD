import math

import pygame

grid_step_x = 3102.0
grid_step_y = 3103.0
list_object = {'База': {}, 'Филд': {}, 'Наземка': {}}

print('Клетка: 13.1х13.1км')
print('Клетка: {0:2.1f}х{1:2.1f}км'.format(grid_step_x/1000,grid_step_y/1000))
print(list_object)
for key, value in list_object.items():
    print(key)

#base_x = 0.5
#base_y = 0.5

#base_x = 0.5
#base_y = 0.25

#base_x = 0.25
#base_y = 0.25

#base_x = 0.25
#base_y = 0.5

#base_x = 0.25
#base_y = 0.75

#base_x = 0.5
#base_y = 0.75

#base_x = 0.75
#base_y = 0.75

#base_x = 0.75
#base_y = 0.5

base_x = 0.75
base_y = 0.25


player_x = 0.5
player_y = 0.5
a = abs(player_y - base_y)
b = abs(player_x - base_x)
player_distance = math.sqrt(a * a + b * b)
quarter = 0
sign = 0
if player_x > base_x and player_y > base_y:
    quarter = 90
    sign = -1
else:
    if player_x > base_x and player_y < base_y:
        quarter = 90
        sign = 1
    else:
        if player_x < base_x and player_y < base_y:
            quarter = 270
            sign = -1
        else:
            quarter = 270
            sign = 1
if b == 0 and a == 0:
    quarter = 90
    alpha = 90
    sign = -1
else:
    if b == 0 and player_y > base_y:
        quarter = 90
        alpha = 90
        sign = -1
    else:
        if a == 0 and player_x > base_x:
            quarter = 90
            alpha = 0
            sign = -1
        else:
            if b == 0 and player_y < base_y:
              quarter = 90
              alpha = 90
              sign = 1
            else:
                alpha = math.atan(a / b) * 180 / math.pi

course = quarter + sign * alpha
print(player_distance,course)

# def main():
#     pygame.init()
#     clock = pygame.time.Clock()
#     joysticks = []
#     for i in range(0, pygame.joystick.get_count()):
#         joysticks.append(pygame.joystick.Joystick(i))
#         joysticks[-1].init()
#     while 1:
#         clock.tick(60)
#         for event in pygame.event.get():
#
#             if event.type == pygame.JOYAXISMOTION:
#                 if event.axis == 1:
#                     print("L Вертикаль", event.value)
#                 elif event.axis == 0:
#                     print("L Горизонталь", event.value)
#             elif event.type == pygame.JOYBUTTONDOWN:
#                 print("Кнопка ВКЛ: ", event.button)
#             elif event.type == pygame.JOYBUTTONUP:
#                 print("Кнопка ВЫКЛ: ", event.button)
#                 if event.button == 7:  # кнопка <START>
#                     print("Выход")
#                     return
#             elif event.type == pygame.JOYHATMOTION:
#                 print("hat: ", event.hat)
#
#
# if __name__ == "__main__":
#     main()