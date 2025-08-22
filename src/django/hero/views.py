from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import Hero
from .serializers import HeroSerializer


class HeroViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing hero operations.
    """
    serializer_class = HeroSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Hero.objects.filter(user=self.request.user)

    @extend_schema(
        tags=['hero'],
        description='Get current user\'s hero',
        responses={
            200: HeroSerializer,
            404: OpenApiResponse(description='Hero not found')
        }
    )
    def list(self, request, *args, **kwargs):
        """
        Get the current user's hero. Each user has only one hero.
        """
        queryset = self.get_queryset()
        hero = queryset.first()
        if hero:
            serializer = self.get_serializer(hero)
            return Response(serializer.data)
        return Response({}, status=404)

    @extend_schema(
        tags=['hero'],
        description='Alternative endpoint to get current user\'s hero',
        responses={
            200: HeroSerializer,
            404: OpenApiResponse(description='Hero not found')
        }
    )
    @action(detail=False, methods=['get'])
    def my_hero(self, request):
        """
        Alternative endpoint to get the authenticated user's hero.
        This endpoint will return a 404 if the hero doesn't exist.
        """
        hero = get_object_or_404(Hero, user=request.user)
        serializer = self.get_serializer(hero)
        return Response(serializer.data)
