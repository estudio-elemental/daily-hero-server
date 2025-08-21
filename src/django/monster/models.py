from django.db import models

from src.core.monsters.domain.monster import Monster as MonsterEntity
from src.django.fight.models import Fight

class Monster(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")
    level = models.IntegerField(default=1, verbose_name="Nível")
    exp_earn = models.IntegerField(default=10, verbose_name="Experiência Ganha")
    hp = models.IntegerField(default=100, verbose_name="Pontos de Vida")
    attack = models.IntegerField(default=20, verbose_name="Ataque")
    defense = models.IntegerField(default=15, verbose_name="Defesa")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Monstro"
        verbose_name_plural = "Monstros"
        ordering = ['level', 'name']

    def __str__(self):
        return f"{self.name} (Nível {self.level})"

    @property
    def is_alive(self):
        return self.hp > 0

    def to_entity(self):
        return MonsterEntity(
            name=self.name,
            level=self.level,
            exp_earn=self.exp_earn,
            hp=self.hp,
            max_hp=self.max_hp,
            _attack=self.attack,
            _defense=self.defense
        )

class FightMonster(models.Model):
    fight = models.ForeignKey(Fight, on_delete=models.CASCADE, related_name='fight_monsters')
    monster = models.ForeignKey('Monster', on_delete=models.CASCADE)
    hp = models.IntegerField(default=5, verbose_name="Pontos de Vida")
    max_hp = models.IntegerField(default=5, verbose_name="Pontos de Vida Máximos")
    name = models.CharField(max_length=100)
    level = models.IntegerField()
    exp_earn = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()

    def __str__(self):
        return f"{self.name} (Fight: {self.fight.id})"

    @property
    def is_alive(self):
        return self.hp > 0

    @classmethod
    def create_from_monster(cls, fight, monster):
        return cls.objects.create(
            fight=fight,
            monster=monster,
            hp=monster.hp,
            max_hp=monster.hp,  # Inicializa max_hp com o hp do monstro
            name=monster.name,
            level=monster.level,
            exp_earn=monster.exp_earn,
            attack=monster.attack,
            defense=monster.defense
        )

    def to_entity(self):
        return MonsterEntity(
            name=self.name,
            level=self.level,
            exp_earn=self.exp_earn,
            hp=self.hp,
            max_hp=self.max_hp,
            _attack=self.attack,
            _defense=self.defense
        )