from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset= CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
