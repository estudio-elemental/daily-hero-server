from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from src.django.monster.models import Monster
from src.django.hero.models import Hero
from src.django.fight.service import FightService

from .serializers import FightRequestSerializer, FightResponseSerializer, StartFightRequestSerializer, StartFightResponseSerializer
from .models import Fight

class FightView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FightRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        fight_service = FightService(fight_id=serializer.validated_data['fight_id'])
        response_data = fight_service.handle_turn()

        response_serializer = FightResponseSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

class StartFightView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = StartFightRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hero_id = serializer.validated_data['hero_id']
        monster_id = serializer.validated_data['monster_id']
        try:
            hero = Hero.objects.get(id=hero_id)
        except Hero.DoesNotExist:
            return Response({"error": "Hero not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if hero.hp <= 0:
            return Response({"error": "Hero is not alive"}, status=status.HTTP_400_BAD_REQUEST)

        if monster_id:
            try:
                monster = Monster.objects.get(id=monster_id)
            except Monster.DoesNotExist:
                return Response({"error": "Monster not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if monster.level > hero.level:
            return Response({"error": "Monster level is too high for the hero"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        fight = Fight.objects.create(
            hero_id=serializer.validated_data['hero_id'],
            monster_id=serializer.validated_data['monster_id'],
            winner=None
        )
        response_serializer = StartFightResponseSerializer({
            'fight_id': fight.id,
            'hero_hp': hero.hp,
            'monster_hp': monster.hp,
            'turn': fight.turn,
            'winner': fight.winner,
            'hero_max_hp': hero.max_hp,
            'monster_max_hp': monster.max_hp
        })
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
