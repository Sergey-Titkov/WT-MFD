import pygame


def main():
    pygame.init()
    joysticks = {}
    joysticksState = {}
    joysticksState_ = {}
    Work = True

    for i in range(0, pygame.joystick.get_count()):
        joy = pygame.joystick.Joystick(i)
        joy.init()
        joysticks[joy.get_instance_id()] = joy
        z = {}
        for row in range(128):
            z[row] = 0
        joysticksState[
            joy.get_name()] = '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        joysticksState_[
            joy.get_name()] = z
        print(joy.get_name(), ' ', joy.get_instance_id())

    while Work:
        #            QtCore.QThread.msleep(100)
        for event in pygame.event.get():
            joyAction = False
            if event.type == pygame.JOYBUTTONDOWN:
                joyAction = True
                print("Кнопка ВКЛ: ", event.button, ' ', joysticks[event.instance_id].get_name())
                tmp = joysticksState[joysticks[event.instance_id].get_name()]
                result = tmp[:event.button] + '1' + tmp[event.button + 1:]
                joysticksState[joysticks[event.instance_id].get_name()] = result

                joysticksState_[joysticks[event.instance_id].get_name()][event.button]=1

                print(joysticks[event.instance_id].get_name(), ": ",
                      joysticksState[joysticks[event.instance_id].get_name()])
                print(joysticks[event.instance_id].get_name(), ": ",
                      joysticksState_[joysticks[event.instance_id].get_name()])

            if event.type == pygame.JOYBUTTONUP:
                joyAction = True
                print("Кнопка ВЫКЛ: ", event.button, ' ', joysticks[event.instance_id].get_name())
                tmp = joysticksState[joysticks[event.instance_id].get_name()]
                result = tmp[:event.button] + '0' + tmp[event.button + 1:]
                joysticksState[joysticks[event.instance_id].get_name()] = result

                joysticksState_[joysticks[event.instance_id].get_name()][event.button] = 0

                print(joysticks[event.instance_id].get_name(), ": ",
                      joysticksState[joysticks[event.instance_id].get_name()])
                print(joysticks[event.instance_id].get_name(), ": ",
                      joysticksState_[joysticks[event.instance_id].get_name()])
            if joyAction:
                for map in mapping:
                    map[2] = joysticksState_[map[0]][map[1]]
                    print()
                Action = True
                for map in mapping:
                    Action = Action and map[2]
                    if not Action:break
                if Action:
                    print("Кнопки 50 и 51 нажаты")
                    Work = False



if __name__ == "__main__":
    mapping = [["S-TECS MODERN THROTTLE MAX STEM",50,0], ["S-TECS MODERN THROTTLE MAX STEM",51,0]]
    z = {}
    for row in range(128):
        z[row] = 0
    #z = {0: 0, 1: 0}
    print(mapping)
    print(z)
    main()
# S-TECS MODERN THROTTLE MAX STEM
