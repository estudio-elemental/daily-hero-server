from abc import abstractmethod

from src.core.shared.creature_interface import ICreature


class IHero(ICreature):
    level: int
    exp: int

    @abstractmethod
    def level_up(self):
        pass

    @abstractmethod
    def rest(self):
        pass