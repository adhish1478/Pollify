# votes/models.py
from django.db import models
from django.conf import settings
from polls.models import Poll, PollOption
# Create your models here.

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    poll= models.ForeignKey(Poll, on_delete=models.CASCADE)
    option= models.ForeignKey(PollOption, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together= ('user', 'poll')  # Ensure a user can only vote once per option in a poll