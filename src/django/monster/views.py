from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Monster
from .serializers import MonsterSerializer

class MonsterFilter(filters.FilterSet):
    """Filter set for Monster model."""
    level = filters.NumberFilter(help_text="Filter by exact level")
    level_min = filters.NumberFilter(field_name='level', lookup_expr='gte', help_text="Filter by minimum level")
    level_max = filters.NumberFilter(field_name='level', lookup_expr='lte', help_text="Filter by maximum level")

    class Meta:
        model = Monster
        fields = ['level', 'level_min', 'level_max']


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination for monster list."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema(
    tags=['monster'],
    parameters=[
        OpenApiParameter(name='level', description='Filter by exact monster level', required=False, type=int),
        OpenApiParameter(name='level_min', description='Filter by minimum monster level', required=False, type=int),
        OpenApiParameter(name='level_max', description='Filter by maximum monster level', required=False, type=int),
        OpenApiParameter(name='page', description='Page number', required=False, type=int),
        OpenApiParameter(name='page_size', description='Number of results per page', required=False, type=int)
    ]
)
class MonsterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing monsters.
    Only returns monsters with level less than or equal to the authenticated user's hero level.
    """
    queryset = Monster.objects.all()
    serializer_class = MonsterSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filterset_class = MonsterFilter
    filter_backends = [DjangoFilterBackend]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @extend_schema(
        description='List monsters available to the current hero based on their level',
        responses={200: MonsterSerializer(many=True)}
    )
    def get_queryset(self):
        # Get hero's level for the authenticated user
        hero = self.request.user.hero
        # Return monsters of the same level as the hero
        return Monster.objects.filter(level__lte=hero.level).order_by('level')
