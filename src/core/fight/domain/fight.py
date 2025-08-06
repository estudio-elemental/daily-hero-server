from dataclasses import dataclass
from time import sleep

from src.core.hero.domain.hero_interface import IHero
from src.core.monsters.domain.monster_interface import IMonster


@dataclass
class Fight:
    hero: IHero
    monster: IMonster

    def start(self):
        round = 1
        print(f"Luta de {self.monster.name} vs nosso Herói!")
        while True:
            print(f"Rodadaaa {round}!!!!")
            print()

            sleep(1)
            print(f"Ataque do {self.monster.name}")
            self.monster.attack(self.hero)
            if self.hero.hp <= 0:
                break
            print()

            sleep(3)
            print(f"Ataque do herói")
            self.hero.attack(self.monster)
            if self.monster.hp <= 0:
                self.hero.gain_exp(self.monster.exp_earn)
                break
            print()

            sleep(3)
            round += 1

        print()
        sleep(3)
