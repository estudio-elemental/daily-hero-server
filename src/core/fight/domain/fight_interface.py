from abc import ABC, abstractmethod


class IFight(ABC):

    @abstractmethod
    def start(self):
        pass
