import random
import abc


class AbstractDungeon(abc.ABC):

    def __init__(self, size: tuple):
        self.size = size
        self.dungeon_map = []
        self.current_map = []

    @abc.abstractmethod
    def create_dungeon(self):
        """
        Generates dungeon. The size of dungeon is given by tuple self.size.
        Entrance is always located at position (1,1)
        """
        raise NotImplementedError

    @abc.abstractmethod
    def place_entities(self, entities: list):
        """
        Place entities in list to random places in created dungeon.
        Player is placed at position (1,1).
        """
        raise NotImplementedError

    @abc.abstractmethod
    def hero_action(self, direction):
        """
        Method to update the position of hero in the map.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update_map(self, entities: list):
        """
        Update map with new position of entities.
        """
        raise NotImplementedError


class Creature(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, identifier: str, position: list, base_attack: int, base_ac: int, damage: int):
        self.map_identifier = identifier
        self.position = position
        self.base_attack = base_attack
        self.base_ac = base_ac
        self.damage = damage

    def attack(self):
        """
        :return: random number representing 1d20 as attack and random number 1d6 as damage
        """
        return {"attack_roll": self.base_attack + random.randint(1, 20),
                "inflicted_damage": sum([random.randint(1, 6) for x in range(self.damage)])}


class SpecialEntity(abc.ABC):

    def __init__(self, identifier: str, position: list, job: str):
        self.map_identifier = identifier
        self.position = position
        self.job = job

    def do_job(self):
        raise NotImplementedError


class Spell(abc.ABC):

    @abc.abstractmethod
    def __init__(self, damage: int, effect: str, cooldown: int):
        self.damage = damage
        self.effect = effect
        self.cooldown = cooldown

    @abc.abstractmethod
    def use_spell(self):
        raise NotImplementedError


class Item(abc.ABC):

    @abc.abstractmethod
    def __init__(self, name: str, slot: str, position, effect: {}):
        self.name = name
        self.slot = slot
        self.position = position
        self.effect = effect
