from abstract_classes import AbstractDungeon
from map_entities import Hero, Goblin, Beholder
from random import choice, randint
from copy import deepcopy
import pickle
import random
from time import strftime
from spellset import Fireball, Teleport
from dungeon_items import *


class Dungeon(AbstractDungeon):
    """
    A class to create a dungeon.

    ...
    Attributes
    -----------
    size: tuple
        width, height of the dungeon
    tunnel_number: int
        number of randomly generated paths
    hero_name: str
        the name of dungeon hero
    file_load: bool
        optional parameter, if True, loading file is selected and loaded


    Other Parameters
    ---------------
    hero:
        class Hero from map_entities module
    items:
        items are dynamically created by the "starting_items" key from  dungeon_items module
    entities:
        entities from map_entities, dynamically created
    Beholder:
        Entity  class Beholder from special_entities
        Gets stronger with hero resting (hp, firebolt dmg scales with hp, melee damage)
        Can be killed with attack, default 20hp, dealing melee damage
        Does not respawn

    Methods
    ------------
    __str__():
        prints current map
    create_dungeon():
        creates map, places entities, items etc.
    set_HUD():
        definnes a HUD with hero parameters and dungeon depth
    find_next():
        returns a location of value on dungeon map
    find_shortest_path():
        return shortest path set from A to B in the dungeon, BFS algorythm
    find_level2():
        find level 2 of BFS algorythm
    hero_action()
        define a hero action in the dungeon
    """

    def __init__(self, size: tuple, tunnel_number: int, hero_name: str, load = False):
        super().__init__(size)
        self.load = load
        if self.load == False:
            # object type Hero from map_entitie
            self.hero = Hero(identifier="@", name=hero_name, position=[1, 1], base_attack=2, base_ac=5, damage=5,
                             spell_set=["fireball", "teleport"])
            # monster BEHOLDER that hunts the player, object from map_entities
            self.beholder = Beholder(identifier="B", position=[1, 1])
            self.tunnel_number = tunnel_number
            self.message = ""
            self.current_spell = ""
            # used for item interaction
            self.current_item = None
            self.HUD = None
            self.depth = 1
            # floor depth
            self.levels = {}
            # for saving the position of stairs down
            self.door_sp = ""
            # starting items, key has to equal to class name
            # values currently just to make it easier to see which item is which
            self.start_item = {"Weapon": "sword",
                               "Weapon2": "javelin",
                               "BodyArmour": "chest-plate",
                               "Ring1": "DurRing",
                               "Ring2": "ACring"}
            self.items = []
            self.entities = []
            self.empty_space = []
            # starting entities, will be remade to objects
            self.starting_entities = ["goblin", "goblin", "goblin"]
            self.create_dungeon()

    def __str__(self):
        """

        Returns
        -------
        Map printable into a console

        """

        printable_map = ""
        for column in self.current_map:
            for row in column:
                printable_map += row
            printable_map += "\n"
        return printable_map

    def set_HUD(self):

        """

        Yields
        -------
        self.HUD parameter to be printed with hero and dungeon info
        """

        equipment = []
        inventory = []
        stats = []

        # information about equipped items
        for key, value in self.hero.equipment.items():
            if isinstance(self.hero.equipment[key], Item):
                equipment.append([value.slot, value.name])
            else:
                equipment.append(None)
        # information about items owned
        for key, value in self.hero.inventory.items():
            if isinstance(self.hero.inventory[key], Item):
                inventory.append([key, value.name])
            else:
                inventory.append(None)
        # creates HUD as a dict
        self.HUD = {"Inventory: ": inventory,
                    "Equipment: ": equipment,
                    "Floor: ": self.depth}
        # list of all parameters of the class hero
        for i in self.hero.__dir__():
            if i == "inventory":
                break
            stat = (str(i), getattr(self.hero, i))
            stats.append(stat)
        # slices and appends 3 stats per row
        for index, i in enumerate(stats):

            if index % 3 == 0 and index != 0:
                self.HUD[f"Stats{index}"] = stats[index - 3:index]

    def create_dungeon(self):
        """
        Returns
        --------
        a dungeon represented in a tuple as self.dungeon_map
        Wall is represented by the "▓" symbol, empty space is represented by the "." symbol (dot).
        Size of the dungeon is (width x height).
        The starting index in the dungeon is (1, 1).
        Every empty space must be accessible from another empty space.
        The edges of the dungeon is bounded by walls.

        Parameters
        ----------
        width: the desired width of the dungeon (the length of one line)
        height: the desired height of the dungeon (the number of lines printed)

        Returns
        -------
        Random dungeon is printed in the console with the size width * height.
        The randomness is pseudorandom brought in by the random module in python.

        Examples
        --------
        >create_dungeon(10, 10)
        ▓▓▓▓▓▓▓▓▓▓
        ▓........▓
        ▓.▓.▓▓.▓.▓
        ▓▓▓.▓▓.▓.▓
        ▓▓▓.▓▓.▓.▓
        ▓▓▓.▓▓.▓.▓
        ▓▓.......▓
        ▓.▓▓▓▓.▓.▓
        ▓......▓.▓
        ▓▓▓▓▓▓▓▓▓▓

        >create_dungeon(10, 10)
        ▓▓▓▓▓▓▓▓▓▓
        ▓........▓
        ▓..▓▓.▓▓.▓
        ▓..▓▓.▓▓.▓
        ▓..▓▓.▓▓.▓
        ▓..▓▓.▓▓.▓
        ▓..▓▓....▓
        ▓..▓▓.▓▓.▓
        ▓▓▓▓▓▓▓..▓
        ▓▓▓▓▓▓▓▓▓▓

        >create dungeon(30, 10)
        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
        ▓............................▓
        ▓.▓▓▓▓▓▓▓.▓.▓▓▓▓.▓▓.▓▓▓▓.....▓
        ▓.▓▓▓▓▓▓▓.▓.▓▓▓▓.▓▓.▓▓▓▓.▓▓▓.▓
        ▓.▓▓▓▓▓▓▓.▓.▓▓▓▓.▓▓.▓▓▓▓.▓▓▓.▓
        ▓.▓▓▓▓▓▓▓.▓.▓▓▓▓.▓▓.▓▓▓▓.▓▓▓.▓
        ▓....................▓▓▓.▓▓▓.▓
        ▓.▓▓▓▓▓▓▓.▓.▓▓▓▓.▓▓..▓▓▓▓▓▓▓.▓
        ▓............................▓
        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

        """
        # function create_dungeon
        # print random dungeon
        width = self.size[0]
        height = self.size[1]
        wall_char = "▓"
        empty_char = "."
        max_tunnel = self.tunnel_number
        direction_choices = ["up", "down", "right", "left"]

        # a record of "motion" that generates tunnels throughout the dungeon is stored in the path_set

        path_set = [[1, 1]]

        # used as a tool to generate the path set
        # refers to the character position in the dungeon

        position = [1, 1]

        while max_tunnel > 0:

            # chooses a random direction from the direction_choices list, tunnel range, it would be pointless
            # to generate tunnels longer than the dungeon, that's why max range is width - 2
            # does so for all the individual tunnels

            direction = choice(direction_choices)
            tunnel_range = randint(1, width - 2)

            # the high coordinate changes
            # with up subtracts
            # with down adds up  (index of the line)

            if direction == "up":
                if tunnel_range > position[0] - 1:
                    tunnel_range = position[0] - 1
                for i in range(1, tunnel_range + 1):
                    position[0] -= 1
                    if position[0:2] not in path_set:
                        path_set.append(position[0:2])
            elif direction == "down":
                if tunnel_range > (height - position[0] - 2):
                    tunnel_range = height - position[0] - 2
                for i in range(1, tunnel_range + 1):
                    position[0] += 1
                    if position[0:2] not in path_set:
                        path_set.append(position[0:2])
            # the width coordinate changes
            # with right adds up
            # with left subtracts   (index on the line)

            elif direction == "right":
                if tunnel_range > (width - position[1] - 2):
                    tunnel_range = width - position[1] - 2

                for i in range(1, tunnel_range + 1):
                    position[1] += 1
                    if position[0:2] not in path_set:
                        path_set.append(position[0:2])
            elif direction == "left":
                if tunnel_range > (position[1] - 1):
                    tunnel_range = position[1] - 1

                for i in range(1, tunnel_range + 1):
                    position[1] -= 1
                    if position[0:2] not in path_set:
                        path_set.append(position[0:2])
            # has to be here for the cycle to end
            max_tunnel -= 1

        self.empty_space = deepcopy(path_set)

        # iterates to print out the lines

        for i in range(height):

            # temp for each iteration stores what's on the line with index [i]
            line = []
            # the index if an element on the line (let "abcd", index of b is 1)
            line_index = 0

            while line_index < width:

                for path in path_set:

                    if path[0] == i and path[1] == line_index:

                        line.append(empty_char)
                        line_index += 1

                        break

                    elif path == path_set[-1]:

                        line.append(wall_char)
                        line_index += 1
                        break

                else:
                    line.append(wall_char)
                    line_index += 1

            self.dungeon_map.append(line)

        # Beholder
        self.beholder.position = choice(self.empty_space)

        # Current map
        self.current_map = deepcopy(self.dungeon_map)
        self.place_entities(self.starting_entities)
        self.place_items()

        # if on deeper floor than 1, 1st tile is a door to go to the previous floor
        if self.depth > 1:
            self.dungeon_map[1][0] = "□"
            self.empty_space.append([1, 0])

        # finds a tile for stairs for entering the next floor, possibly further from the hero
        try:
            door_pos = choice(list(filter(lambda x: x[0] > 10 and x[1] > 10, self.empty_space)))
        except IndexError:
            try:
                door_pos = choice(list(filter(lambda x: x[0] > 10 or x[1] > 10, self.empty_space)))
            except IndexError:
                door_pos = choice(list(filter(lambda x: x[0] > 0 or x[1] > 0, self.empty_space)))
        # find a wall next to the tile
        self.door_sp = self.find_next(door_pos, wall_char)
        # if a tile is found, create "■" character to represent stairs down, else append it to the start
        if self.door_sp:
            self.dungeon_map[self.door_sp[0]][self.door_sp[1]] = "■"
        else:
            self.door_sp = [0, 1]
            self.dungeon_map[self.door_sp[0]][self.door_sp[1]] = "■"
        # make the beholder to be able to enter the position (could crash orthervise)
        # has to be at the end to prevent entities and items to be placed there
        self.empty_space.append(self.door_sp)

        self.update_map()

    def find_shortest_path(self, start, end):
        """
        Breath First Search algorythm for the dungeon represented in the Manhattan matric
        Parameters
        ----------
        start: list
            the starting position in the dungeon
        end: list
            the ending position
        Returns
        -------
        The shortest path through empty spaces in the dungeon from Start to the End
        """
        # directions of each tile
        direction_choices = []
        # "value" of each search level
        path_value = 1
        # tiles that were already visited
        visited = [start]
        # nodes of one iteration
        nodes = []
        # directory stores all levels
        path = {"0": start}

        # all the accesible places from the starting point make the first direction choices
        for x in [[start[0] - 1, start[1]],
                  [start[0], start[1] - 1],
                  [start[0] + 1, start[1]],
                  [start[0], start[1] + 1]]:
            if x in self.empty_space and x not in visited:
                direction_choices.append(x)

        path[str(path_value)] = direction_choices[:]
        path_value += 1

        # search until reach the end coord
        while end not in visited:

            # que stores nodes for each iteration
            # all neighbouring nodes will be stored in direction choices
            queue = deepcopy(direction_choices)
            direction_choices.clear()

            for index, v in enumerate(queue):

                for n in [[v[0] + 1, v[1]],
                          [v[0] - 1, v[1]],
                          [v[0], v[1] + 1],
                          [v[0], v[1] - 1]]:
                    if n in self.empty_space and n not in visited:
                        nodes.append(n)
                        visited.append(n)

            path[str(path_value)] = nodes[:]
            path_value += 1

            for i in nodes:
                direction_choices.append(i)
            nodes.clear()

        short_path = [end]
        path_values = list(path.values())
        path_values.reverse()

        # reverts all values in path to go from last level (contains end) to the start
        # chronologically searches for the neighbouring tiles of the desired coords

        for value in path_values:
            for point in value:
                prev_point = short_path[-1]

                if point in [[prev_point[0] + 1, prev_point[1]],
                             [prev_point[0] - 1, prev_point[1]],
                             [prev_point[0], prev_point[1] + 1],
                             [prev_point[0], prev_point[1] - 1]]:
                    short_path.append(point)
        short_path.reverse()
        return short_path[:]

    def find_level2(self, start):

        """

        Parameters
        ----------
        start

        Returns
        -------
        Level 2 of the BFS algorythm (see find_shortest_path)

        """
        direction_choices = []
        path_value = 1
        visited = [start]
        nodes = []
        path = {"0": start}
        for x in [[start[0] - 1, start[1]],
                  [start[0], start[1] - 1],
                  [start[0] + 1, start[1]],
                  [start[0], start[1] + 1]]:
            if x in self.empty_space and x not in visited:
                direction_choices.append(x)

        path[str(path_value)] = direction_choices[:]
        path_value += 1

        queue = deepcopy(direction_choices)
        direction_choices.clear()

        for index, v in enumerate(queue):

            for n in [[v[0] + 1, v[1]],
                      [v[0] - 1, v[1]],
                      [v[0], v[1] + 1],
                      [v[0], v[1] - 1]]:
                if n in self.empty_space and n not in visited:
                    nodes.append(n)
                    visited.append(n)

        path[str(path_value)] = nodes[:]

        return path["2"]

    def find_next(self, start, tile: str):
        """

        Parameters
        ----------
        start: tuple
            tile
        tile: str
            value

        Returns
        -------
        Neighbouring object to the start of the desired value

        """
        direction_choices = [[start[0] - 1, start[1]],
                             [start[0], start[1] - 1],
                             [start[0] + 1, start[1]],
                             [start[0], start[1] + 1]]

        for node in direction_choices:
            try:
                if self.dungeon_map[node[0]][node[1]] == tile:
                    return node

            except IndexError:
                continue

        # if it doesn't find an object, return any object that isnt a wall
        else:
            for node in direction_choices:

                try:
                    if self.dungeon_map[node[0]][node[1]] != "▓":
                        return node
                except IndexError:
                    continue

    def beholder_action(self, action):

        """
        define an action of beholder

        If the parameter is move, beholder moves by the find_shortesr_path to the hero by 2 tiles.
        If the parameter is firebolt beholder moves by 2 tiled to the hero (find_shortest_path) or attacks with firebolt
        and move by 1 tile
        If the parameter is random, beholder moves by 2 tiles in random direction.
        Parameters
        ----------
        action: str
            defines an action of beholder
            move,random or firebolt



        """

        if action == "move":
            bpath = self.find_shortest_path(start=self.beholder.position, end=self.hero.position)
            self.beholder.position = bpath[1]
            self.message += "the beholder is moving"

        elif action == "firebolt":
            bpath = self.find_shortest_path(start=self.beholder.position, end=self.hero.position)
            # if there is no wall between hero and beholder, attack with firebolt, else move
            if all(x in list(filter(lambda x: x[0] == self.hero.position[0], self.empty_space)) for x in bpath) \
                    or \
                    all(x in list(filter(lambda x: x[1] == self.hero.position[1], self.empty_space)) for x in bpath):

                self.beholder.position = bpath[0]

                # beholder has 20 hp

                bolt_damage = randint(0 + int(self.beholder.hp//20), 5 + int(self.beholder.hp//20) )
                self.hero.hp -= bolt_damage
                self.message += f"the beholder attacked with firebolt, dealing {bolt_damage} damage"

            else:
                self.beholder.position = bpath[1]
                self.message += "the beholder is moving"

        elif action == "random":

            self.beholder.position = choice(self.find_level2(self.beholder.position))

    def hero_action(self, action):

        """
        defines an action of hero in the dungeon.

        Parameters
        ----------
        action:

        move  (L)EFT, (R)IGHT, (D)OWN, (U)P
        after movement comes beholder action

        attack (A)TTACK
        item interaction (E)QUIP, (UE)QUIP, (DR)OP, (P)ICKUP
        spells (S)PELLS
        """

        if action == "R":
            if self.dungeon_map[self.hero.position[0]][self.hero.position[1] + 1] != "▓":
                self.hero.position[1] += 1

        if action == "L":
            if self.dungeon_map[self.hero.position[0]][self.hero.position[1] - 1] != "▓":
                self.hero.position[1] -= 1

        if action == "D":
            if self.dungeon_map[self.hero.position[0] + 1][self.hero.position[1]] != "▓":
                self.hero.position[0] += 1

        if action == "U":
            if self.dungeon_map[self.hero.position[0] - 1][self.hero.position[1]] != "▓":
                self.hero.position[0] -= 1

        if action in ["U", "D", "R", "L", "RE", "S"]:

            # go to the next level, ■ stairs down
            if self.dungeon_map[self.hero.position[0]][self.hero.position[1]] == "■" and \
                    f"{self.depth + 1}" not in list(self.levels.keys()):
                # save current floor, reset, create next

                save_file = {"curr_map": self.current_map,
                             "map": self.dungeon_map,
                             "beholder": self.beholder,
                             "entities": self.entities,
                             "items": self.items,
                             "start_entities": self.starting_entities,
                             "empty": self.empty_space,
                             "beholder_position": self.beholder.position,
                             "door_sp": self.door_sp}

                self.levels[f"{self.depth}"] = save_file
                self.depth += 1
                self.dungeon_map = []
                self.current_map = []
                self.entities = []
                self.empty_space = []
                self.items = []
                self.hero.position = [1, 1]
                self.create_dungeon()

            elif self.dungeon_map[self.hero.position[0]][self.hero.position[1]] == "■" and \
                    f"{self.depth + 1}" in list(self.levels.keys()):

                # save progress of current floor, load next

                save_file = {"curr_map": self.current_map,
                             "map": self.dungeon_map,
                             "beholder": self.beholder,
                             "entities": self.entities,
                             "items": self.items,
                             "start_entities": self.starting_entities,
                             "empty": self.empty_space,
                             "beholder_position": self.beholder.position,
                             "door_sp": self.door_sp}

                self.levels[f"{self.depth}"] = save_file
                self.depth += 1
                self.dungeon_map = self.levels[f"{self.depth}"]["map"]
                self.current_map = self.levels[f"{self.depth}"]["curr_map"]
                self.entities = self.levels[f"{self.depth}"]["entities"]
                self.starting_entities = self.levels[f"{self.depth}"]["start_entities"]
                self.empty_space = self.levels[f"{self.depth}"]["empty"]
                self.beholder = self.levels[f"{self.depth}"]["beholder"]
                self.beholder.position = self.levels[f"{self.depth}"]["beholder_position"]
                self.items = self.levels[f"{self.depth}"]["items"]
                self.door_sp = self.levels[f"{self.depth}"]["door_sp"]
                self.hero.position = [1, 1]

            # go to the previous level, □ stairs up

            elif self.dungeon_map[self.hero.position[0]][self.hero.position[1]] == "□" and \
                    f"{self.depth - 1}" in list(self.levels.keys()):

                # save progress of current floor, load previous

                save_file = {"curr_map": self.current_map,
                             "map": self.dungeon_map,
                             "beholder": self.beholder,
                             "entities": self.entities,
                             "items": self.items,
                             "start_entities": self.starting_entities,
                             "empty": self.empty_space,
                             "beholder_position": self.beholder.position,
                             "door_sp": self.door_sp}

                self.levels[f"{self.depth}"] = save_file
                self.depth -= 1
                self.dungeon_map = self.levels[f"{self.depth}"]["map"]
                self.current_map = self.levels[f"{self.depth}"]["curr_map"]
                self.entities = self.levels[f"{self.depth}"]["entities"]
                self.starting_entities = self.levels[f"{self.depth}"]["start_entities"]
                self.empty_space = self.levels[f"{self.depth}"]["empty"]
                self.beholder = self.levels[f"{self.depth}"]["beholder"]
                self.beholder.position = self.levels[f"{self.depth}"]["beholder_position"]
                self.items = self.levels[f"{self.depth}"]["items"]
                self.door_sp = self.levels[f"{self.depth}"]["door_sp"]
                # finds an empty tile next to the stairs down on previous level
                self.hero.position = self.find_next(self.door_sp, ".")

            else:

                if self.beholder.hp > 0:
                    # BEHOLD THE BEHOLDER
                    if action == "RE":
                        # beholder gets stronger when hero rests

                        self.beholder.hp += 4
                        self.beholder.damage += 2

                    # if there is distance lower than 15, warning message is printed
                    if (lambda x, y: abs(x - self.hero.position[0]) + abs(y - self.hero.position[1]))(
                            self.beholder.position[0],
                            self.beholder.position[
                                1]) <= 15:
                        self.message += "the beholder sees you \n"
                    # if there is distance lower than 11, beholder moves towards the hero
                    if 11 >= (lambda x, y: abs(x - self.hero.position[0]) + abs(y - self.hero.position[1]))(
                            self.beholder.position[0],
                            self.beholder.position[1]) > 6:
                        self.beholder_action("move")
                    # if there is distance lower than 6, beholder uses firebolt, move if wall (see beholder action)
                    elif (lambda x, y: abs(x - self.hero.position[0]) + abs(y - self.hero.position[1]))(
                            self.beholder.position[0],
                            self.beholder.position[
                                1]) <= 6:
                        if self.beholder.position == self.hero.position:
                            dmg = self.beholder.melee
                            self.hero.hp -= dmg
                            self.message += f"the beholder hit, dealing {dmg}"
                        else:
                            self.beholder_action("firebolt")
                    # beholder buffs us every time hero rests

                    else:
                        # else move randomly

                        self.beholder_action("random")

        if action == "A":
            # fight with entity if in entity position
            if self.hero.position == self.beholder.position:
                self.hero.hp -= self.beholder.damage
                hero_roll = self.hero.attack()
                self.beholder.hp -= hero_roll["inflicted_damage"]
            if self.beholder.hp <= 0:
                self.current_map[self.beholder.position[0]][self.beholder.position[1]] = "C"

            for entity in self.entities:
                if self.hero.position == entity.position:
                    if hasattr(entity, "attack"):
                        self.fight(entity)
                        break
            else:
                self.message = "You are hitting air really hard!"

        if action == "P":
            # if the inventory is full, print message
            if all(list(self.hero.inventory.values())):
                self.message += "I am no beast of burden"
            else:

                # if in item position, pickup item
                for item in self.items:
                    if self.hero.position == item.position:
                        # uses current item to interact with
                        self.current_item = item
                        # remove item from iteration to be able to represent items in the level progression
                        self.items.remove(item)
                        # remove item from the dungeon
                        item.position = "picked"
                        self.hero.pick_up(self.current_item)
                        self.dungeon_map[self.hero.position[0]][self.hero.position[1]] = "."

                self.current_item = None
                # if item guarded by an entity, fight the entity
                for entity in self.entities:
                    if self.hero.position == entity.position:
                        if hasattr(entity, "attack"):
                            self.fight(entity)
                            break

        if action == "DR":

            if self.current_item not in list(self.hero.inventory.values()):
                self.message += "No such item in possession"

            else:
                # drop item, append to the items list
                self.hero.drop_item(self.current_item)
                # has to deepcopy else item position moves with hero position
                # once hero position is reverted from a save file
                self.current_item.position = deepcopy(self.hero.position)
                self.dungeon_map[self.hero.position[0]][self.hero.position[1]] = self.current_item.identifier
                self.items.append(self.current_item)
                self.current_item = None

                # doesn't overwrite entity if item is dropped on it, instead mark location with X
                for entity in self.entities:
                    if self.hero.position == entity.position:
                        self.dungeon_map[self.hero.position[0]][self.hero.position[1]] = "X"
                        break

        if action == "E":
            # equips item if item in inventory

            if self.current_item not in list(self.hero.inventory.values()):
                self.message += "No such item in possession"
            else:
                # if the item is from class item, equip on the right slot
                if isinstance(self.hero.equipment[self.current_item.slot], Item):
                    self.dungeon_map[self.hero.position[0]][self.hero.position[1]] = self.hero.equipment[
                        self.current_item.slot].identifier
                    self.hero.equipment[self.current_item.slot].position = self.hero.position

                self.hero.equip(self.current_item)
                self.current_item.position = "equipped"
                self.current_item = None

        if action == "UE":
            # unequip an item from hero equipment

            if self.current_item not in list(self.hero.equipment.values()):
                self.message += "No such item in possession"
            else:
                # unequiping drops item on the ground
                self.hero.un_equip(self.current_item)
                self.dungeon_map[self.hero.position[0]][self.hero.position[1]] = self.current_item.identifier
                self.current_item.position = deepcopy(self.hero.position)
                self.items.append(self.current_item)
                self.current_item = None

        if action == "S":
            # use a spell from hero spell set
            # create a class from the string inserted

            if self.current_spell == "fireball":

                self.current_spell = Fireball(10, "damage", 5)
            elif self.current_spell == "teleport":

                self.current_spell = Teleport(0, "teleport", 5)
            # check what the spell actually is
            spell_identity = self.current_spell.use_spell()
            # if the spell is not a damaging spell, use the spell
            if spell_identity["spell_damage"] == 0:
                self.message = f"{self.current_spell.effect} used"
                if spell_identity["spell_effect"] == "teleport":
                    self.hero.position = choice(self.empty_space)

            else:
                # find an entity to damage, entity doesn't fight back
                for entity in self.entities:

                    if self.hero.position == entity.position:
                        entity.hp -= self.current_spell.damage
                        self.message += f"{self.current_spell} used, inflicted {self.current_spell.damage} dmg \n"

                        if entity.hp <= 0:
                            self.message += f"{entity} has been slain"
                            self.dungeon_map[entity.position[0]][entity.position[1]] = "."
                            self.entities.remove(entity)
                        else:
                            self.message += f"Monster hp: {entity.hp}"
                        break
                else:
                    self.message += "That would be a waste of mana"
        # update map after every action
        self.update_map()

    def place_entities(self, entities: list):

        """
        places entities on the dungeon map as objects from module map_entities

        Parameters
        ----------
        entities: list

            starting entities of the dungeon, strings

        """

        # beholder already placed, remove from selection
        self.empty_space.remove(self.beholder.position)
        # create positions for entities
        positions = random.sample(self.empty_space, len(self.starting_entities))
        self.empty_space.append(self.beholder.position)
        self.current_map[self.beholder.position[0]][self.beholder.position[1]] = self.beholder.map_identifier
        # creates instances of entity classes, append them to the entities list
        for idx, entity in enumerate(self.starting_entities):
            if entity == "goblin":
                self.entities.append(
                    Goblin(identifier="\033[38;5;1mg\033[0;0m", position=positions[idx], base_attack=1, base_ac=5,
                           damage=2))
        # visualizes entities on the map by their identifier
        for entity in self.entities:
            self.dungeon_map[entity.position[0]][entity.position[1]] = entity.map_identifier

    def place_items(self):

        """
        Dynamically creates instances of classes from the dungeon_items module.
        Items are represented by string as a name of the class in the starting_items dict
        Chooses random items from item list (at least 2)
        """

        positions = random.sample(self.empty_space, len(self.start_item))
        # random number of items, in range of 1/2 of maximum number of items, minimum 2
        idx_choices = random.randint(2, len(self.start_item)//2)
        item_choices = list(self.start_item.keys())
        # read class name of the items
        for idx in range(idx_choices):
            try:
                # find a key in the list of global function in the module, choose at random
                key = choice(list(self.start_item.keys()))
                klass = globals()[f"{key}"]
                # create instance
                item = klass()
                # append items into item list, represent position on the map
                if hasattr(item, "position"):
                    item.position = positions[idx - 1]
                    self.items.append(item)

            except KeyError:
                continue
        # represent items on the map by their string identifier
        for item in self.items:
            self.dungeon_map[item.position[0]][item.position[1]] = item.identifier

    def update_map(self):

        """

        updates position of moving units

        """

        self.current_map = deepcopy(self.dungeon_map)
        self.current_map[self.hero.position[0]][self.hero.position[1]] = self.hero.map_identifier
        if self.beholder.hp > 0:
            self.current_map[self.beholder.position[0]][self.beholder.position[1]] = self.beholder.map_identifier

    def fight(self, monster):
        """
        fight between hero and entity
        roll the dice, return damage

        Parameters
        ----------
        monster

        """
        hero_roll = self.hero.attack()
        monster_roll = monster.attack()

        if hero_roll["attack_roll"] > monster.base_ac:
            monster.hp -= hero_roll["inflicted_damage"]
            if monster.hp > 0:
                # monster receives damage
                self.message = f"Hero inflicted {hero_roll['inflicted_damage']}"
            else:
                # monster death
                self.message = f"Hero inflicted {hero_roll['inflicted_damage']} and slain {monster}"
                self.hero.gold += monster.gold
                self.hero.xp += 1
                self.dungeon_map[monster.position[0]][monster.position[1]] = "."
                self.entities.remove(monster)
        if monster_roll["attack_roll"] > self.hero.base_ac:
            self.message += f"\n Monster inflicted {monster_roll['inflicted_damage']}"
            # hero receives damage
            self.hero.hp -= monster_roll['inflicted_damage']
            # hero death
            if self.hero.hp < 1:
                self.message += f"{self.hero.name} has been slain"
        self.message += f"\n Hero HP: {self.hero.hp}  Monster HP: {monster.hp}"
