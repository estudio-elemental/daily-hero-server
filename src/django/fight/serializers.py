from rest_framework import serializers
from .models import Fight

class FightRequestSerializer(serializers.Serializer):
    fight_id = serializers.IntegerField()

class FightResponseSerializer(serializers.Serializer):
    hero_hp = serializers.IntegerField()
    monster_hp = serializers.IntegerField()
    turn = serializers.CharField()  # 'monster', 'hero', or 'over'
    winner = serializers.CharField(allow_null=True)  # null until the end of the fight
    hero_max_hp = serializers.IntegerField()
    monster_max_hp = serializers.IntegerField()

class StartFightRequestSerializer(serializers.Serializer):
    hero_id = serializers.IntegerField()
    monster_id = serializers.IntegerField()

class StartFightResponseSerializer(serializers.Serializer):
    fight_id = serializers.IntegerField()
    hero_hp = serializers.IntegerField()
    monster_hp = serializers.IntegerField()
    turn = serializers.CharField() 
    winner = serializers.CharField(allow_null=True)
    hero_max_hp = serializers.IntegerField()
    monster_max_hp = serializers.IntegerField()
