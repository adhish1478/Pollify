from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

# Create your models here.
class CreateUserManager(BaseUserManager):
    def create_user(self, email,password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email= self.normalize_email(email)
        user= self.model(email= email, **extra_fields)
        user.set_password(password)
        user.save(using= self._db)

        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractUser):
    username= None
    email= models.EmailField(unique=True)
    bio= models.TextField(blank=True, max_length=500)
    profile_picture= models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_verified= models.BooleanField(default=False)
    is_staff= models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)

    objects= CreateUserManager()
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS= []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email