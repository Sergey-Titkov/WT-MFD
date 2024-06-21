import pygame

grid_step_x = 3102.0
grid_step_y = 3103.0
list_object = {'База': {}, 'Филд': {}, 'Наземка': {}}

print('Клетка: 13.1х13.1км')
print('Клетка: {0:2.1f}х{1:2.1f}км'.format(grid_step_x/1000,grid_step_y/1000))
print(list_object)
for key, value in list_object.items():
    print(key)




def main():
    pygame.init()
    clock = pygame.time.Clock()
    joysticks = []
    for i in range(0, pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
        joysticks[-1].init()
    while 1:
        clock.tick(60)
        for event in pygame.event.get():

            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 1:
                    print("L Вертикаль", event.value)
                elif event.axis == 0:
                    print("L Горизонталь", event.value)
            elif event.type == pygame.JOYBUTTONDOWN:
                print("Кнопка ВКЛ: ", event.button)
            elif event.type == pygame.JOYBUTTONUP:
                print("Кнопка ВЫКЛ: ", event.button)
                if event.button == 7:  # кнопка <START>
                    print("Выход")
                    return
            elif event.type == pygame.JOYHATMOTION:
                print("hat: ", event.hat)


if __name__ == "__main__":
    main()