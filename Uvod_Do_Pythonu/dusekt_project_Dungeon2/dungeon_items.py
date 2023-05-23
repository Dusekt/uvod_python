from abstract_classes import Item

"""
Module to represent dungeon items.
Items are all defined and take 0 arguments.
Derived from the abstract class Item from abstract_classes module

Parameters
-----------
name: str
    name of an item
slot: str
    name of a slot the item goes in
position: None
    var to represent where the item is
identifier: str
    usually first letter of the slot, represent item visually when printed on the map
effect: dict
    key - string, has to correspond to some of the Hero stats from map_entities module
    value - int, number added to the stat

Notes
------
is used as an "attribute" for Hero in map_entities module
"""

class Weapon(Item):

    def __init__(self):
        self.name = "sword"
        self.slot = "weapon"
        self.position = None
        self.identifier = "w"
        self.effect = {"damage": 3}


class Weapon2(Item):

    def __init__(self):
        self.name = "javelin"
        self.slot = "weapon"
        self.position = None
        self.identifier = "w"
        self.effect = {"damage": 5}


class BodyArmour(Item):

    def __init__(self):
        self.name = "armour"
        self.slot = "body"
        self.position = None
        self.identifier = "A"
        self.effect = {"hp": 10}

class Ring1(Item):

    def __init__(self):
        self.name = "DurRing"
        self.slot = "ring_1"
        self.position = None
        self.identifier = "R"
        self.effect = {"max_hp": 12}

class Ring2(Item):

    def __init__(self):
        self.name = "ACRing"
        self.slot = "ring_2"
        self.position = None
        self.identifier = "R"
        self.effect = {"base_ac": 1}

