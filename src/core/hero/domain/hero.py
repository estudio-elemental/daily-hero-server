from dataclasses import dataclass
from random import randint
from time import sleep

from src.core.hero.domain.hero_interface import IHero
from src.core.monsters.domain.monster_interface import IMonster


@dataclass
class Hero(IHero):
    level: int
    exp: int
    hp: int
    max_hp: int
    _attack: int
    _defense: int

    def attack(self, monster: IMonster) -> None:
        damage = randint(self._attack//3, self._attack)
        print(f"Acerta um golpe com {damage} de dano")
        sleep(1)
        monster.defend(damage)

    def defend(self, damage: int) -> None:
        defence = randint(self._defense//3, self._defense)
        print(f"Herói defende {defence} de dano.")
        sleep(1)
        total_damage = damage - defence
        self.hp -= total_damage if total_damage > 0 else 0
        if self.hp <= 0:
            print("Herói morreu")
            sleep(1)
        else:
            print(f"Hp do Herói: {self.hp}")
            sleep(1)

    def level_up(self):
        self.level += 1
        self.max_hp += 5
        self._attack += 2
        self._defense += 1
        print(f"Herói evolui para o level {self.level}.")
        sleep(1)

    def rest(self):
        self.hp = self.max_hp

    def gain_exp(self, exp: int):
        self.exp += exp
        if self.exp >= 100 * self.level:
            self.exp = 0
            self.level_up()
