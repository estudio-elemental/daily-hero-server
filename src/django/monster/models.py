from django.db import models

from src.core.monsters.domain.monster import Monster as MonsterEntity

class Monster(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")
    level = models.IntegerField(default=1, verbose_name="Nível")
    exp_earn = models.IntegerField(default=10, verbose_name="Experiência Ganha")
    hp = models.IntegerField(default=100, verbose_name="Pontos de Vida")
    max_hp = models.IntegerField(default=100, verbose_name="Pontos de Vida Máximos")
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