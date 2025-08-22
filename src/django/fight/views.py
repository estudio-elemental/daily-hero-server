from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse

from src.django.monster.models import Monster, FightMonster
from src.django.hero.models import Hero
from src.django.fight.service import FightService

from .serializers import FightRequestSerializer, FightResponseSerializer, StartFightRequestSerializer, StartFightResponseSerializer
from .models import Fight


class FightView(APIView):
    """View for handling fight turns."""
    
    @extend_schema(
        tags=['fight'],
        description='Execute a turn in the fight',
        request=FightRequestSerializer,
        responses={
            200: FightResponseSerializer,
            400: OpenApiResponse(description='Invalid fight ID'),
            404: OpenApiResponse(description='Fight not found')
        }
    )
    def post(self, request, *args, **kwargs):
        """Execute a turn in the fight.
        
        This endpoint processes one turn in the ongoing fight, updating health points
        and determining if there's a winner.
        """
        serializer = FightRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        fight_service = FightService(fight_id=serializer.validated_data['fight_id'])
        response_data = fight_service.handle_turn()

        response_serializer = FightResponseSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class StartFightView(APIView):
    """View for initiating a new fight between a hero and a monster."""
    
    @extend_schema(
        tags=['fight'],
        description='Start a new fight between a hero and a monster',
        request=StartFightRequestSerializer,
        responses={
            201: StartFightResponseSerializer,
            400: OpenApiResponse(description='Invalid request - Hero is not alive or monster level is too high'),
            404: OpenApiResponse(description='Hero or monster not found')
        }
    )
    def post(self, request, *args, **kwargs):
        """Start a new fight between a hero and a monster.
        
        This endpoint validates that:
        - Both hero and monster exist
        - Hero is alive (has HP > 0)
        - Monster level is not higher than hero's level
        
        If all conditions are met, creates a new fight instance and returns its details.
        """
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

        try:
            monster = Monster.objects.get(id=monster_id)
        except Monster.DoesNotExist:
            return Response({"error": "Monster not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if monster.level > hero.level:
            return Response({"error": "Monster level is too high for the hero"}, status=status.HTTP_400_BAD_REQUEST)

        fight = Fight.objects.create(
            hero_id=hero_id,
            monster_id=monster_id,
            winner=None
        )
        fight_monster = FightMonster.create_from_monster(fight=fight, monster=monster)

        response_serializer = StartFightResponseSerializer({
            'fight_id': fight.id,
            'hero_hp': hero.hp,
            'monster_hp': fight_monster.hp,
            'turn': fight.turn,
            'winner': fight.winner,
            'hero_max_hp': hero.max_hp,
            'monster_max_hp': fight_monster.max_hp
        })
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
