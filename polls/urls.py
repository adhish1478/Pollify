from .views import PollListCreateView, PollDetailView
from django.urls import path

urlpatterns=[
    path('', PollListCreateView.as_view(), name='poll-list-create'),
    path('<int:pk>/', PollDetailView.as_view(), name='poll-detail'),
]