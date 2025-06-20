from .views import PollViewSet, poll_detail
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router= DefaultRouter()
router.register(r'', PollViewSet)


urlpatterns=[
    path('', include(router.urls)),
    path('poll-page/<int:poll_id>/', poll_detail, name='poll-detail')
]