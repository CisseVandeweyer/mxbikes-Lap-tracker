from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.views import APIView
from .serializers import LapSerializer

# Create your views here.
class LapCreateView(APIView):
    def post (self, request):
        serializer = LapSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class UserLapsView(APIView):
    def get(self, request, discord_id=None, username=None):
        username = username or request.query_params.get("username")
        try:
            if discord_id:
                user = User.objects.get(discord_id=discord_id)
            elif username:
                user = User.objects.get(username=username)
            else:
                return Response({"error": "Geen discord_id of username opgegeven"}, status=400)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        laps = Lap.objects.filter(user=user)
        serializer = LapSerializer(laps, many=True)
        return Response(serializer.data, status=200)
    
class UserDetailView(APIView):
    def get(self, request, discord_id):
        try:
            user = User.objects.get(discord_id=discord_id)
            return Response({"username": user.username}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)