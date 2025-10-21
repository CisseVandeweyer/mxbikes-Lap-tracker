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