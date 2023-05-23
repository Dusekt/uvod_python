import random
from abstract_classes import Creature, SpecialEntity
from dungeon_items import *


class Hero(Creature):
    """
    A class to create hero.

    Attributes:
    -----------
    identifier: str
        string representation of the hero on the map
    name: str
        hero name
    position: list
        position on the map
    base_attack: int
    base_ac: int
    damage: int
    spell_set: bool / list
        can be bool or list, if false, hero cant cast spells

    Methods:
    --------
    level_up(): raises level
    rest(): restores mana and hp
    pick_up(): place item into inventory
    drop_item(): drop item on ground
    equip(): equip item, improves stats
    unequip(): unequip item

    """

    object_type = "hero"

    def __init__(self, identifier, name, position, base_attack, base_ac, damage, spell_set=False):
        super().__init__(identifier, position, base_attack, base_ac, damage)
        self.name = name
        self.max_hp = 20
        self.hp = 20
        self.max_stamina = 20
        self.stamina = 20
        self.xp = 0
        self.level = 1
        self.gold = 0
        self.spells = spell_set
        self.inventory = {"1": None,
                          "2": None,
                          "3": None,
                          "4": None,
                          "5": None,
                          "6": None}

        self.equipment = {"body": None,
                          "helmet": None,
                          "gloves": None,
                          "boots": None,
                          "ring_1": None,
                          "ring_2": None,
                          "amulet": None,
                          "weapon": None,
                          "offhand": None}

    def level_up(self):
        self.level += 1
        self.xp = 0
        self.max_hp += 5

    def rest(self):
        self.hp = self.max_hp
        self.stamina = self.max_stamina

    def pick_up(self, item):

        for key, value in self.inventory.items():
            if not value:
                self.inventory[key] = item
                break

    def drop_item(self, item):

        for key, value in list(self.inventory.items()):
            if value == item:
                self.inventory[key] = None
                break

    def equip(self, item):

        for key in list(self.equipment.keys()):

            # if item in item slot is item, unequip old item
            if key == item.slot:
                if isinstance(self.equipment[key], Item):
                    self.un_equip(self.equipment[key])

                self.equipment[key] = item
                # if equiped item is class Item
                if isinstance(item, Item):
                    for stat, val in item.effect.items():
                        # if hero stat matches stat in item.effect, increase the hero's stat by the value
                        if stat in self.__dir__():
                            exec(f"self.{stat} += {val}")
                break

        # remove item from inventory (equipped)
        for key, value in self.inventory.items():
            if value == item:
                self.inventory[key] = None
                break

    def un_equip(self, item):

        for key, value in list(self.equipment.items()):
            if value == item:
                self.drop_item(item)
                self.equipment[key] = None
                if isinstance(item, Item):
                    # subscript value from un-equipped item from hero stats
                    for stat, val in item.effect.items():
                        if stat in self.__dir__():
                            exec(f"self.{stat} -= {val}")
                break


class Goblin(Creature):
    object_type = "monster"

    def __str__(self):
        return "Goblin"

    def __init__(self, identifier, position, base_attack, base_ac, damage):
        super().__init__(identifier, position, base_attack, base_ac, damage)
        self.hp = random.randint(1, 5)
        self.xp = 10
        self.gold = random.randint(1, 6)


class Beholder(SpecialEntity):
    """
    defines special entity Beholder that haunts the player
    """

    def __init__(self, identifier, position, job="hunt"):
        super().__init__(identifier, position, job)
        # damage is pure, removes dmg from hero hp if attacked on melee range
        self.damage = 15
        # has to high roll or have a weapon to kill Beholder
        self.hp = 20
        self.melee = random.randint(2, 10)

    def do_job(self):
        return self.job


if __name__ == '__main__':

    hero = Hero(identifier="@", name="wda", position=[1, 1], base_attack=2, base_ac=5, damage=5,
                spell_set=["fireball", "teleport"])
    stats = []
    print(hero.__dir__())
    for i in hero.__dir__():
        if i == "inventory":
            break
        stat = (str(i), getattr(hero, i))
        stats.append(stat)

    print(stats)
