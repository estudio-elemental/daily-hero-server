from dataclasses import dataclass
from random import randint
from time import sleep

from src.core.monsters.domain.monster_interface import IMonster
from src.core.hero.domain.hero_interface import IHero


@dataclass
class Monster(IMonster):
    level: int
    exp_earn: int
    name: str
    hp: int
    _attack: int
    _defense: int

    def attack(self, hero: IHero) -> None:
        damage = randint(self._attack//3, self._attack)
        print(f"Acerta um golpe com {damage} de dano")
        sleep(1)
        hero.defend(damage)

    def defend(self, damage: int) -> None:
        defence = randint(self._defense//3, self._defense)
        print(f"{self.name} defende {defence} de dano.")
        sleep(1)
        total_damage = damage - defence
        self.hp -= total_damage if total_damage > 0 else 0
        if self.hp <= 0:
            print(f"{self.name} morreu")
            sleep(1)

        else:
            print(f"Hp do {self.name}: {self.hp}")
            sleep(1)
