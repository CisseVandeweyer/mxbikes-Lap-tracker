from django.urls import path, include
from .views import LapCreateView


urlpatterns = [
    path('laps/create', LapCreateView.as_view(), name='create lap'),
]