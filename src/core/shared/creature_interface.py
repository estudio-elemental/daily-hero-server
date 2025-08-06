from abc import ABC, abstractmethod


class ICreature(ABC):
    max_hp: int
    hp: int
    _attack: int
    _defense: int

    @abstractmethod
    def attack(self, creature: "ICreature"):
        pass

    @abstractmethod
    def defend(self, damage: int):
        pass
