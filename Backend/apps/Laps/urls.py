from django.urls import path, include
from .views import *


urlpatterns = [
    # Endpoint om een rondetijd toe te voegen
    path('laps/create/', LapCreateView.as_view(), name='create-lap'),

    # Endpoint om rondetijden van een specifieke gebruiker op te halen via discord_id
    path('laps/user/<str:discord_id>/', UserLapsView.as_view(), name='user-laps'),

    # Optioneel: endpoint om alle laps van een gebruiker op username op te halen
    path('laps/user_by_username/<str:username>/', UserLapsView.as_view(), name='user-laps-username'),

    path('users/<str:discord_id>/', UserDetailView.as_view(), name='user-detail'),

]