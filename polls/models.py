from django.db import models
from accounts.models import CustomUser as User
# Create your models here.
class Poll(models.Model):
    question= models.CharField(max_length=200)
    image= models.ImageField(upload_to='polls_images/', blank=True, null=True)
    created_at = models.DateTimeField('date published', auto_now_add=True)
    created_by= models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls_created')

    def __str__(self):
        return self.question
    
class PollOption(models.Model):
    poll= models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    option_text= models.CharField(max_length=200)

    def __str__(self):
        return self.option_text