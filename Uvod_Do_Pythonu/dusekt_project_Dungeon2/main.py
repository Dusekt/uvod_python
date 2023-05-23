"""
module used to initialize the DUNGEON game, printed in the console, actions are printed before every move
"""

import subprocess
from pathlib import Path
import sys
from dusekt_Dungeon import Dungeon
import pickle
from time import strftime

if __name__ == "__main__":

    GAME = ""
    HUD = ""
    FLAG = True
    # used for restarting the game
    while FLAG is True:
        # not restart by default
        FLAG = False

        if GAME != "NEWGAME":
            GAME = input("start a new game (NEWGAME)"
                         " or load game from a save file (LOAD)"
                         " or (EXIT): ")

        if GAME == "NEWGAME":

            hero_name = input("what is your hero? ")
            dungeon: Dungeon = Dungeon(size=(40, 10),
                                       tunnel_number=40,
                                       hero_name=hero_name)
        # load game from a load file, pickled
        elif GAME == "LOAD":

            loading_files = []
            for item in Path("./Dungeon_saves").iterdir():
                loading_files.append(item)
            # print out files to load from, choose a index of a file to load from
            for index, file in enumerate(loading_files[:]):
                if index + 1 == 1:
                    INDEX_FIRST = 1
                if file == loading_files[-1]:
                    INDEX_LAST = index + 1
                print(f"{file}: INDEX = {index + 1}")

            while True:

                print(f"type number type integer in range {INDEX_FIRST}, {INDEX_LAST}")
                LOAD_NUM = input(
                    "select a file to load from: (INDEX (1, 2, 3...)) for new game type NEWGAME ")

                if LOAD_NUM == "NEWGAME":
                    break

                try:
                    LOAD_NUM = int(LOAD_NUM)
                    if LOAD_NUM in range(INDEX_FIRST, INDEX_LAST + 1):
                        break
                # if not a number or NEWGAME, roll over it is
                except ValueError:
                    continue

            if LOAD_NUM == str("NEWGAME"):
                FLAG = True
                GAME = "NEWGAME"
                continue

            for index, file in enumerate(loading_files):
                if index + 1 == int(LOAD_NUM):
                    LOAD = str(file)
                    break
            # used as a metric
            with open(f"{LOAD}", "rb") as f:

                dungeon = pickle.load(f)

            print(dungeon)

        elif GAME == "EXIT":
            sys.exit()
        # restart loop
        else:

            FLAG = True
            continue
        # printing, GAME
        while True:

            subprocess.Popen("Cls", shell=True).communicate()
            print(dungeon.levels.keys())
            # printable hud, managed by the C action
            if HUD:

                dungeon.set_HUD()
                HUD = dungeon.HUD

            dun = str(dungeon)
            hud_idx = -1

            # print dungeon, if HUD print HUD line by line behind the dungeon line
            for index, i in enumerate(dun):
                print(i, end="")
                if HUD:

                    try:
                        # select by "hud index" the number of line, 1st and last lines are "outline" of the HUD
                        if dun[index+1] == "\n" and hud_idx < 0:
                            print("   ","*"*80, end="")
                            hud_idx += 1
                            # prints out elements from the HUD.items, hud being a dict
                        elif dun[index+1] == "\n" and hud_idx < len(HUD):
                            print(f"    {list(HUD.items())[hud_idx]}",end="")
                            hud_idx += 1
                            # last line of the DUNGEON is the last line of the HUD
                        elif dun[index+1] == "\n" and hud_idx == dungeon.size[1]-2:
                            print("   ", "*" * 80)

                        elif dun[index+1] == "\n":
                            hud_idx += 1

                    except IndexError:

                        break
            # used to print whats happening in the dungeon
            print(dungeon.message)
            dungeon.message = ""

            if dungeon.hero.hp <= 0:
                print("YOU DIED")

                while True:
                    restart = input("do you wish to start over? Y/N  ")
                    if restart in ("Y", "N"):
                        break

                if restart == "Y":
                    FLAG = True
                    break

                if restart == "N":
                    sys.exit()
            # hero action options
            action = input(
                f"select an action for {dungeon.hero.name}: "
                f"(L)EFT,"
                f" (R)IGHT,"
                f" (D)OWN,"
                f"(U)P,"
                f"(Q)UIT,"
                f" (A)TTACK: ,"
                "(E)QUIP: ,"
                "(P)ICKUP: ,"
                "(UE)QUIP: ,"
                "(DR)OP: ,"
                "(S)PELL: ,"
                "(C)HAR: ,"
                "(RE)ST: ")

            if action == "Q":

                while True:

                    save: str = input("Save the progress? Y/N ")
                    if save in ("Y", "N"):
                        break

                if save == "Y":
                    time_string = strftime("%Y%m%d-%H%M%S")
                    dungeon.load = True
                    with open(f"./Dungeon_saves/{dungeon.hero.name}_{time_string}.dng", "wb") as f:
                        pickle.dump(dungeon,f)

                print("You coward!")
                sys.exit()

            elif action == "DR":
                # item slot selection, if no item, there is an empty slot
                for key, value in dungeon.hero.inventory.items():
                    try:
                        print(f"{key}: {value.name}")
                    except AttributeError:
                        print(f"{key}: {None}")

                itm = input("select item from your inventory")
                # selects item from inventory by index
                while not dungeon.current_item:
                    try:
                        dungeon.current_item = dungeon.hero.inventory[itm]
                        break
                    except KeyError:
                        itm = input("please select valid slot")
                # can not drop empty slot
                try:
                    dungeon.hero_action(action)
                except AttributeError:
                    dungeon.message = "That is an empty slot"

            elif action == "E":
                for key, value in dungeon.hero.inventory.items():
                    try:
                        print(f"{key}:  {value.name}")
                    except AttributeError:
                        print(f"{key}:  {None}")

                itm = input("select item from your inventory")

                while not dungeon.current_item:
                    try:
                        dungeon.current_item = dungeon.hero.inventory[itm]
                        break
                    except KeyError:
                        itm = input("please select valid slot")

                try:
                    dungeon.hero_action(action)
                except AttributeError:
                    dungeon.message = "That is an empty slot"

            elif action == "UE":
                for key, value in dungeon.hero.equipment.items():
                    try:
                        # abs here used for indentation
                        print(f"{key}:{(' '*abs(10 - len(key)))[:-1]}{value.name}")
                    except AttributeError:
                        print(f"{key}:{(' '*abs(10 - len(key)))[:-1]}{None}")

                itm = input("select item from your inventory")
                while not dungeon.current_item:
                    try:
                        dungeon.current_item = dungeon.hero.equipment[itm]
                        break
                    except KeyError:
                        itm = input("please select valid slot")
                try:
                    dungeon.hero_action(action)
                except AttributeError:
                    dungeon.message = "that is an empty slot"

            elif action == "S":

                if dungeon.hero.spells:

                    while True:
                        for i in dungeon.hero.spells:
                            print(i)
                        dungeon.current_spell = input("choose a spell to use: ")
                        if dungeon.current_spell in dungeon.hero.spells:
                            break

                    dungeon.hero_action(action)

                else:
                    dungeon.message = "you have no spells to use"

            elif action == "RE":
                dungeon.hero.rest()
                dungeon.hero_action("RE")

            elif action == "C":

                # Toggle the HUD printing

                if HUD:
                    HUD = None
                else:
                    HUD = True
            else:
                dungeon.hero_action(action)
