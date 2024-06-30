import math
from math import sqrt

from WarThunder import telemetry
from WarThunder import mapinfo
from pprint import pprint
import os
import time


def find_map_info():
    print('------------------------------------------------------')
    print('Map Info:')
    print('\tName:\t\t\t\t\t{}'.format(telem.map_info.grid_info['name']))
    print('\tGrid_size:\t\t\t\t\t{}'.format(telem.map_info.info['grid_size']))
    print('\tGrid steps:\t\t\t\t\t{}'.format(telem.map_info.info['grid_steps']))
    print('\tGrid zero:\t\t\t\t\t{}'.format(telem.map_info.info['grid_zero']))
    print('\tMap max:\t\t\t\t\t{}'.format(telem.map_info.info['map_max']))
    print('\tMap min:\t\t\t\t\t{}'.format(telem.map_info.info['map_min']))

    print('\tUpper Left Hand Corner Coordinate:\t[{}, {}]'.format(telem.map_info.grid_info['ULHC_lat'],
                                                                  telem.map_info.grid_info['ULHC_lon']))
    print(
        '\tSize:\t\t\t\t\t{}km x {}km'.format(telem.map_info.grid_info['size_km'], telem.map_info.grid_info['size_km']))
    print('')


def find_all_bomb_points():
    print('------------------------------------------------------')
    find_bomb_points(True)
    find_bomb_points(False)


def find_all_airfields():
    print('------------------------------------------------------')
    find_airfields(True)
    find_airfields(False)


def find_all_planes():
    print('------------------------------------------------------')
    find_planes(True)
    find_planes(False)


def find_all_tanks():
    print('------------------------------------------------------')
    find_tanks(True)
    find_tanks(False)


def find_all_AAAs():
    print('------------------------------------------------------')
    find_AAAs(True)
    find_AAAs(False)


def find_basic_telemetry():
    print('------------------------------------------------------')
    print('Basic Telemetry:')
    pprint(telem.basic_telemetry)
    print('')


def find_comments():
    print('------------------------------------------------------')
    print('Comments:')
    comments = telem.get_comments()

    if comments:
        pprint(comments)
    else:
        print('\tNone')
    print('')


def find_events():
    print('------------------------------------------------------')
    print('Events:')
    events = telem.get_events()

    if events:
        pprint(events)
    else:
        print('\tNone')
    print('')


def find_bomb_points(friendly=True):
    if friendly:
        print('Friendly Bomb Points:')
        bomb_points = [obj for obj in telem.map_info.defend_points() if obj.friendly]
    else:
        print('Enemy Bomb Points:')
        bomb_points = [obj for obj in telem.map_info.bombing_points() if not obj.friendly]

    if bomb_points:
        for bomb_point in bomb_points:
            print('\tBombing Point: {}'.format(bomb_point.position_ll))
            print('\tBombing Point: {}'.format(bomb_point.position))
    else:
        print('\tNone')
    print(' ')


def find_airfields(friendly=True):
    if friendly:
        print('Friendly Airfields:')
        airfields = [obj for obj in telem.map_info.airfields() if obj.friendly]
    else:
        print('Enemy Airfields:')
        airfields = [obj for obj in telem.map_info.airfields() if not obj.friendly]

    if airfields:
        for airfield in airfields:
            print('\tEast Coordinate:\t{}'.format(airfield.east_end_ll))
            print('\tSouth Coordinate:\t{}'.format(airfield.south_end_ll))
            print('\tRunway Heading:\t\t{} °'.format(airfield.runway_dir))
            print('\tRunway Length:\t\t{} km'.format(mapinfo.coord_dist(*airfield.east_end_ll, *airfield.south_end_ll)))
            print('')
    else:
        print('\tNone')
    print('')


def find_planes(friendly=True):
    if friendly:
        print('Friendly Planes:')
        planes = [obj for obj in telem.map_info.planes() if obj.friendly]
    else:
        print('Enemy Planes:')
        planes = [obj for obj in telem.map_info.planes() if not obj.friendly]

    if planes:
        for plane in planes:
            print('\tPosition:\t{}'.format(plane.position_ll))
            print('\tHeading:\t{}'.format(plane.hdg))
            print('')
    else:
        print('\tNone')
    print('')


def find_tanks(friendly=True):
    if friendly:
        print('Friendly Tanks:')
        tanks = [obj for obj in telem.map_info.tanks() if obj.friendly]
    else:
        print('Enemy Tanks:')
        tanks = [obj for obj in telem.map_info.tanks() if not obj.friendly]

    if tanks:
        for tank in tanks:
            print('\tPosition:\t{}'.format(tank.position_ll))
            print('\tHeading:\t{}'.format(tank.hdg))
            print('')
    else:
        print('\tNone')
    print('')


def find_AAAs(friendly=True):
    if friendly:
        print('Friendly AAAs:')
        AAAs = [obj for obj in telem.map_info.AAAs() if obj.friendly]
    else:
        print('Enemy AAAs:')
        AAAs = [obj for obj in telem.map_info.AAAs() if not obj.friendly]

    if AAAs:
        for AAA in AAAs:
            print('\tPosition:\t{}'.format(AAA.position_ll))
    else:
        print('\tNone')
    print('')


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    try:
        telem = telemetry.TelemInterface()

        while not telem.get_telemetry():
            pass

        find_map_info()
        # find_all_airfields()
        # find_all_planes()
        # find_all_tanks()
        while True:
            if telem.get_telemetry(comments=False, events=False):
                find_map_info()
                print('Player:\t')
                print('\tX и Y:\t{},{}'.format(telem.map_info.player_x, telem.map_info.player_y))
                print('\tLat и Lon:\t{},{}'.format(telem.map_info.player_lat, telem.map_info.player_lon))
                find_bomb_points(False)
                grid_steps = telem.map_info.info['grid_steps']
                size_x = telem.map_info.info['map_max'][0] - telem.map_info.info['map_min'][0]
                size_y = telem.map_info.info['map_max'][1] - telem.map_info.info['map_min'][1]

                bomb_points = [obj for obj in telem.map_info.bombing_points() if not obj.friendly]
                if bomb_points:
                    for bomb_point in bomb_points:
                        base_x = bomb_point.position[0]
                        base_y = bomb_point.position[1]
                        player_x = telem.map_info.player_x
                        player_y = telem.map_info.player_y
                        a = abs(player_y - base_y)*size_x
                        b = abs(player_x - base_x)*size_y
                        player_distance = math.sqrt(a * a + b * b)
                        quarter = 0
                        sign = 0
                        if player_x < base_x and player_y > base_y:
                            quarter = 90
                            sign = -1
                        else:
                            if player_x < base_x and player_y < base_y:
                                quarter = 90
                                sign = 1
                            else:
                                if player_x > base_x and player_y < base_y:
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
                                if a == 0 and player_x < base_x:
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

                        player_course = quarter + sign * alpha
                        bomb_point.player_distance = player_distance
                        bomb_point.player_course = player_course
                        # var
                        # ctx = canvas.getContext('2d')
                        # var
                        # w = canvas.width
                        # var
                        # h = canvas.height
                        # var
                        # mapMin = map_info['map_min']
                        # var
                        # mapMax = map_info['map_max']
                        # var
                        # scX = w / (mapMax[0] - mapMin[0])
                        # var
                        # scY = h / (mapMax[1] - mapMin[1])
                        #
                        # ctx.lineWidth = 1
                        # ctx.strokeStyle = '#555'
                        #
                        # ctx.beginPath()
                        # for (var y = mapMin[1]; y <= mapMax[1]; y += map_info['grid_steps'][1]) {
                        #     var yy = Math.floor((y-mapMin[1]) * scY)+0.5
                        # ctx.moveTo(0, yy)
                        # ctx.lineTo(w, yy)
                        # }

                        #base_x * size_x/telem.map_info.info['grid_steps'][0]
                        #base_y * size_y / telem.map_info.info['grid_steps'][1]
                        column = 1+int(base_x * size_x/telem.map_info.info['grid_steps'][0])
                        row = chr(65+int(base_y * size_y / telem.map_info.info['grid_steps'][1]))
                        name = '{}{}'.format(row,column )
                        bomb_point.name = name
                        print('\tBombing Point: {}, distance: {:2.1f}км, course: {:3.0f}'.format(bomb_point.name, bomb_point.player_distance/1000, bomb_point.player_course))
                    else:
                        print('\tNone')
                    print(' ')
                    time.sleep(0.2)
                else:
                    pass
        # find_all_AAAs()
        # find_basic_telemetry()
        # find_comments()
        # find_events()

    except KeyboardInterrupt:
        print('Closing')
# telem.map_info.player_found.
# Тудер
#     var mapMin = map_info['map_min']
# var mapMax = map_info['map_max']
# var scX = w / (mapMax[0] - mapMin[0])
# var scY = h / (mapMax[1] - mapMin[1])
