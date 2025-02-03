import pygame

def main():
     pygame.init()
     clock = pygame.time.Clock()
     joysticks = []
     for i in range(0, pygame.joystick.get_count()):
         joysticks.append(pygame.joystick.Joystick(i))
         joysticks[-1].init()
         print(pygame.joystick.Joystick(i).get_name())
     while 1:
         clock.tick(60)
         for event in pygame.event.get():

             if event.type == pygame.JOYBUTTONDOWN:
                print("Кнопка ВКЛ: ", event.button)

             if event.type == pygame.JOYBUTTONUP and event.dict['joy'] == 1 and event.dict['button'] == 13:

                 print("Кнопка ВЫКЛ: ", event.button)
                 print(event.dict)
#         joystick = pygame.joystick.Joystick(1)
#         if joystick:
#             if joystick.get_button(13):
#                 print("Кнопка 13")


     #        joystick = pygame.joystick.Joystick(0)
     #       if joystick:
#
#
#             if joystick.get_button(13):
     #                print("Кнопка ВЫКЛ: ", event.button)
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


if __name__ == "__main__":
    main()