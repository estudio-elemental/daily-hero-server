from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Hero
from .serializers import HeroSerializer


class HeroViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HeroSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Hero.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        hero = queryset.first()
        if hero:
            serializer = self.get_serializer(hero)
            return Response(serializer.data)
        return Response({}, status=404)

    @action(detail=False, methods=['get'])
    def my_hero(self, request):
        """
        Endpoint para retornar o herói do usuário autenticado
        """
        hero = get_object_or_404(Hero, user=request.user)
        serializer = self.get_serializer(hero)
        return Response(serializer.data)
