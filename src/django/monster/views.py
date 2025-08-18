from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Monster
from .serializers import MonsterSerializer

class MonsterFilter(filters.FilterSet):
    level = filters.NumberFilter()
    level_min = filters.NumberFilter(field_name='level', lookup_expr='gte')
    level_max = filters.NumberFilter(field_name='level', lookup_expr='lte')

    class Meta:
        model = Monster
        fields = ['level', 'level_min', 'level_max']


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class MonsterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Monster.objects.all()
    serializer_class = MonsterSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filterset_class = MonsterFilter
    filter_backends = [DjangoFilterBackend]


    def get_queryset(self):
        # Get hero's level for the authenticated user
        hero = self.request.user.hero
        # Return monsters of the same level as the hero
        return Monster.objects.filter(level__lte=hero.level).order_by('level')
