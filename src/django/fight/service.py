from dataclasses import dataclass
from src.core.fight.domain.fight import Fight
from src.core.hero.domain.hero import Hero
from src.core.monsters.domain.monster import Monster

from src.django.fight.models import Fight as FightModel
from src.django.hero.models import Hero as HeroModel
from src.django.monster.models import Monster as MonsterModel


class FightService:

    def __init__(self, fight_id: int):
        self.fight_model = FightModel.objects.get(id=fight_id)

    def handle_turn(self):
        monster_model = MonsterModel.objects.get(id=self.fight_model.monster_id)
        hero_model = HeroModel.objects.get(id=self.fight_model.hero_id)

        hero = hero_model.to_entity()
        monster = monster_model.to_entity()

        if self.fight_model.turn == 'hero':
            hero.attack(monster)
            if not monster.is_alive:
                self.fight_model.winner = 'hero'
                self.fight_model.turn = 'over'
                hero.gain_exp(monster.exp_earn)

            else:
                self.fight_model.turn = 'monster'
        elif self.fight_model.turn == 'monster':
            monster.attack(hero)
            if not hero.is_alive:
                self.fight_model.winner = 'monster'
                self.fight_model.turn = 'over'
            else:
                self.fight_model.turn = 'hero'

        hero_model.hp = hero.hp
        hero_model.level = hero.level
        hero_model.exp = hero.exp
        hero_model.max_hp = hero.max_hp
        hero_model.attack = hero._attack
        hero_model.defense = hero._defense
        hero_model.save()

        monster_model.hp = monster.hp
        if self.fight_model.turn == 'over':
            monster_model.hp = monster.max_hp  # Reset monster HP if fight is over
        monster_model.save()

        self.fight_model.save()

        return {
            'hero_hp': hero.hp,
            'monster_hp': monster.hp,
            'turn': self.fight_model.turn,
            'winner': self.fight_model.winner
        }
        