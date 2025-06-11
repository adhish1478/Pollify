from django.shortcuts import render
from .models import Poll
from .serializers import PollSerializer
from rest_framework import generics, permissions, status
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response

# Create your views here.
class PollListCreateView(generics.ListCreateAPIView):
    queryset= Poll.objects.all()
    serializer_class= PollSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        serializer.save(created_by= self.request.user)

class PollDetailView(generics.RetrieveDestroyAPIView):
    queryset= Poll.objects.all()
    serializer_class= PollSerializer
    permission_classes= [IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        return Response({"detail": "Updating a poll is not allowed."}, status= status.HTTP_403_FORBIDDEN)
    def patch(self, request, *args, **kwargs):
        return Response({"detail": "Updating a poll is not allowed."}, status= status.HTTP_403_FORBIDDEN)