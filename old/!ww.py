import json
import types
bind = types.SimpleNamespace()
bind.eventOccur = False
bind.keys = [["S-TECS MODERN THROTTLE MAX STEM", 50, 0], ["S-TECS MODERN THROTTLE MAX STEM", 51, 0]]


with open('WriteTimeOffsetToFile.cfg') as f:
    templates = json.load(f)


t = []
for key in templates:
    t.append([key[0], key[1],0])

print(t)

