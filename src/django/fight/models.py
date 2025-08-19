from django.db import models


MONSTER_CHOICES = [
    ('monster', 'Monster'),
    ('hero', 'Hero'),
    ('over', 'Over')
]

WINNER_CHOICES = [
    ('hero', 'Hero'),
    ('monster', 'Monster'),
    (None, 'None')
]


# Create your models here.
class Fight(models.Model):
    hero_id = models.IntegerField()
    monster_id = models.IntegerField()
    turn = models.CharField(max_length=10, choices=MONSTER_CHOICES, default='monster')
    winner = models.CharField(max_length=10, blank=True, null=True, choices=WINNER_CHOICES)

    def __str__(self):
        return f"Fight {self.id}: Hero {self.hero_id} vs Monster {self.monster_id}"
