from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.views import APIView
from .serializers import LapSerializer

# Create your views here.
class SetUsernameView(APIView):
    """Endpoint om een username te zetten als deze nog niet bestaat"""
    def post(self, request, discord_id):
        username = request.data.get("username")
        if not username:
            return Response({"error": "Username niet opgegeven"}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(discord_id=discord_id).exists():
            return Response({"error": "Username bestaat al, gebruik edit endpoint"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User(discord_id=discord_id, username=username)
        user.save()
        return Response({"message": "Username ingesteld"}, status=status.HTTP_201_CREATED)

class EditUsernameView(APIView):
    """Endpoint om een bestaande username te wijzigen"""
    def put(self, request, discord_id):
        new_username = request.data.get("username")
        if not new_username:
            return Response({"error": "Nieuwe username niet opgegeven"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(discord_id=discord_id)
            user.username = new_username
            user.save()
            return Response({"message": "Username bijgewerkt"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class AddLapView(APIView):
    """Endpoint om een lap toe te voegen"""
    def post(self, request):
        discord_id = request.data.get("discord_id")
        username = request.data.get("username")

        # Check of user bestaat
        try:
            user = User.objects.get(discord_id=discord_id)
        except User.DoesNotExist:
            return Response({"error": "Discord gebruiker heeft nog geen username ingesteld"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LapSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # <-- haal user=user weg
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
        
