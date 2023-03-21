# function create_dungeon
# print random dungeon
from random import choice, randint


def create_dungeon(width, height, **kwargs):
    """
    Returns a dungeon printed in text format in the console window.
    Wall is represented by the "▓" symbol, empty space is represented by the "." symbol (dot).
    Size of the dungeon is (width x height).
    The starting index in the dungeon is (1, 1).
    Every empty space must be accessible from another empty space.
    The edges of the dungeon is bounded by walls.

    Parameters
    ----------
    width: the desired width of the dungeon (the length of one line)
    height: the desired height of the dungeon (the number of lines printed)
    **kwargs: multiple key-word arguments are possible, for future development

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
    wall_char = "▓"
    empty_char = "."
    max_tunnel = randint(100, 150)
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
                path_set.append(position[0:2])

        elif direction == "down":
            if tunnel_range > (height - position[0] - 2):
                tunnel_range = height - position[0] - 2
            for i in range(1, tunnel_range + 1):
                position[0] += 1
                path_set.append(position[0:2])

        # the width coordinate changes
        # with right adds up
        # with left subtracts   (index on the line)

        elif direction == "right":
            if tunnel_range > (width - position[1] - 2):
                tunnel_range = width - position[1] - 2

            for i in range(1, tunnel_range + 1):
                position[1] += 1
                path_set.append(position[0:2])

        elif direction == "left":
            if tunnel_range > (position[1] - 1):
                tunnel_range = position[1] - 1

            for i in range(1, tunnel_range + 1):
                position[1] -= 1
                path_set.append(position[0:2])

        # has to be here for the cycle to end

        max_tunnel -= 1

    # iterates to print out the lines

    for i in range(height):

        print()
        # temp for each iteration stores what's on the line with index [i]
        line = []
        # the index if an element on the line (let "abcd", index of b is 1)
        line_index = 0

        while line_index < width:

            # for every iteration go through the path_set
            # if it finds the first element that corresponds to the 'path' (the generated tunnel) with indexes
            # appends "." to the line list

            for path in path_set:

                if path[0] == i and path[1] == line_index:

                    line.append(empty_char)
                    line_index += 1

                    # break is here for a "restart" of the iteration,
                    # for every character the path_set is gone through again

                    break

                # if none corresponding path elements are not found, append a wall character

                elif path == path_set[-1]:

                    line.append(wall_char)
                    line_index += 1
                    break

            # if there were none path elements for the current line, append a wall
            # else here is linked to the for statement checking for path_set

            else:
                line.append(wall_char)
                line_index += 1

        # print the line

        for char in line:
            print(char, end="")

#ha
create_dungeon(80, 20)
