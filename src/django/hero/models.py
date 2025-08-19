from django.db import models
from django.contrib.auth import get_user_model

from src.core.hero.domain.hero import Hero as HeroEntity


User = get_user_model()

class Hero(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    level = models.IntegerField(default=1, verbose_name="Nível")
    exp = models.IntegerField(default=0, verbose_name="Experiência")
    max_hp = models.IntegerField(default=100, verbose_name="HP Máximo")
    hp = models.IntegerField(default=100, verbose_name="HP Atual")
    attack = models.IntegerField(default=20, verbose_name="Ataque")
    defense = models.IntegerField(default=15, verbose_name="Defesa")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Herói"
        verbose_name_plural = "Heróis"

    def __str__(self):
        return f"Herói de {self.user.username} (Nível {self.level})"

    @property
    def is_alive(self):
        return self.hp > 0

    def to_entity(self):
        return HeroEntity(
            level=self.level,
            exp=self.exp,
            max_hp=self.max_hp,
            hp=self.hp,
            _attack=self.attack,
            _defense=self.defense
        )