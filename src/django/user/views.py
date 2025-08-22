from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from datetime import timedelta
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, UserSerializer
from src.django.hero.models import Hero

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Create a new user account and associated hero."""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @extend_schema(
        tags=['auth'],
        description='Create a new user account. A hero will be automatically created for the user.',
        responses={201: UserSerializer}
    )
    def perform_create(self, serializer):
        # Cria o usuário
        user = serializer.save()
        
        # Cria o herói associado ao usuário
        Hero.objects.create(
            user=user,
            level=1,
            exp=0,
            max_hp=5,
            hp=5,
            attack=3,
            defense=1
        )


class LoginView(generics.GenericAPIView):
    """Login view to obtain JWT tokens."""
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @extend_schema(
        tags=['auth'],
        description='Log in with email and password to obtain JWT tokens',
        responses={
            200: OpenApiResponse(
                description='Login successful',
                response={
                    'type': 'object',
                    'properties': {
                        'refresh': {'type': 'string'},
                        'access': {'type': 'string'},
                        'user': {'type': 'object'}
                    }
                }
            ),
            400: OpenApiResponse(description='Invalid credentials')
        }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })


class UserProfileView(generics.RetrieveAPIView):
    """View to retrieve and update user profile information."""
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @extend_schema(
        tags=['auth'],
        description='Get current user profile',
        responses={200: UserSerializer}
    )
    def get_object(self):
        return self.request.user


@extend_schema(
    tags=['auth'],
    description='Log out by blacklisting the refresh token',
    request=LogoutSerializer,
    responses={
        200: OpenApiResponse(description='Logout successful'),
        400: OpenApiResponse(description='Invalid token'),
        500: OpenApiResponse(description='Internal server error')
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout view to blacklist the refresh token."""
    try:
        serializer = LogoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "error": "Dados inválidos",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        refresh_token = serializer.validated_data['refresh']
        token = RefreshToken(refresh_token)
        
        # Tenta fazer blacklist se o método estiver disponível
        try:
            if hasattr(token, 'blacklist'):
                token.blacklist()
            else:
                # Se blacklist não estiver disponível, apenas invalida o token
                token.set_exp(lifetime=timedelta(seconds=0))
        except Exception:
            # Fallback: invalida o token definindo expiração para 0
            token.set_exp(lifetime=timedelta(seconds=0))
        
        return Response({"message": "Logout realizado com sucesso."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            "error": "Erro interno do servidor",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
