from django.urls import path
from .views import FightView, StartFightView

urlpatterns = [
    path('fight/', FightView.as_view(), name='fight'),
    path('start-fight/', StartFightView.as_view(), name='start-fight'),
]
