from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserUpdateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
# Create your views here.

class RegisterView(CreateAPIView):
    queryset= CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

class ProfileView(RetrieveUpdateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = CustomUserUpdateSerializer

    def get_object(self):
        return self.request.user
