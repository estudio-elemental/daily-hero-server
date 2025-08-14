from django.db import models


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
