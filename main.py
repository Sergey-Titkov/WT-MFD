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
        while telem.get_telemetry(comments=False, events=False):
            os.system('cls' )
            find_map_info()
            find_bomb_points(False)
            print(telem.map_info.player_lat)
            print(telem.map_info.player_x)
            print(telem.map_info.player_lon)
            print(telem.map_info.player_y)
            time.sleep(0.2)
            pass
        # find_all_AAAs()
        # find_basic_telemetry()
        # find_comments()
        # find_events()

    except KeyboardInterrupt:
        print('Closing')
#telem.map_info.player_found.
#Тудер
        #     var mapMin = map_info['map_min']
      #var mapMax = map_info['map_max']
        # var scX = w / (mapMax[0] - mapMin[0])
      #var scY = h / (mapMax[1] - mapMin[1])