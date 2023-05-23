from dusekt_Dungeon import Dungeon
from random import choice
from math import inf
from copy import deepcopy

Dungeon = Dungeon(size=(40, 10), tunnel_number=40, hero_name="karel", file_load=False)
print(Dungeon)


def find_shortest_path(start=Dungeon.beholder.position, end = Dungeon.hero.position):
    distance = (lambda x, y: abs(x - end[0]) + abs(y - end[1]))(
        start[0], start[1])

    direction_choices = []
    start = start
    path_value = 1
    visited = [start]
    nodes = []
    path = {"0" : start}
    for x in [[start[0] - 1, start[1]],
              [start[0], start[1] - 1],
              [start[0] + 1, start[1]],
              [start[0], start[1] + 1]]:
        if x in Dungeon.empty_space and x not in visited:
            direction_choices.append(x)

    path[str(path_value)] = direction_choices[:]
    path_value += 1
    # TADY IMPLEMENTOVAT FCI prohledavani

    while end not in visited:

        queue = deepcopy(direction_choices)
        direction_choices.clear()

        #print(queue)
        for index, v in enumerate(queue):
            #print(v)
            for n in [[v[0] + 1,v[1]],
                      [v[0] - 1,v[1]],
                      [v[0], v[1] + 1],
                      [v[0], v[1] - 1]]:
                if n in Dungeon.empty_space and n not in visited:
                    nodes.append(n)
                    visited.append(n)


        path[str(path_value)] = nodes[:]
        path_value += 1

        #print(path)
        for i in nodes:
            direction_choices.append(i)
        nodes.clear()
    a = int((list(path.keys())[-1]))
    short_path = [end]
    path_values = list(path.values())
    path_values.reverse()

    for value in path_values:
        for point in value:
            prev_point = short_path[-1]

            if point in [[prev_point[0] + 1,prev_point[1]],
                      [prev_point[0] - 1,prev_point[1]],
                      [prev_point[0], prev_point[1] + 1],
                      [prev_point[0], prev_point[1] - 1]]:
                short_path.append(point)
    short_path.reverse()
    return short_path[:]


if __name__ == '__main__':
    print(find_shortest_path(start=Dungeon.beholder.position, end=Dungeon.hero.position))
    print(Dungeon.beholder.position)



