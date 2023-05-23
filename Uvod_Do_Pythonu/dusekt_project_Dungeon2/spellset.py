from abstract_classes import Spell

class Fireball(Spell):

    def __init__(self, damage, effect, cooldown):
        self.damage = damage
        self.effect = effect
        self.cooldown = cooldown

    def use_spell(self):
        return {"spell_damage": self.damage, "spell_effect": self.effect}

class Teleport(Spell):

    def __init__(self, damage, effect, cooldown):
        self.damage = damage
        self.effect = effect
        self.cooldown = cooldown

    def use_spell(self):
        return {"spell_damage": self.damage, "spell_effect": self.effect}

#print(fireball.cooldown)



