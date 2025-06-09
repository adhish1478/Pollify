from .models import CustomUser
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only= True)
    class Meta:
        model= CustomUser
        fields= ('email','password', 'bio', 'profile_picture')

    def create(self, validates_data):
        user= CustomUser.objects.create_user(
            email= validates_data['email'],
            password= validates_data['password'],
            bio= validates_data.get('bio', ''),
            profile_picture= validates_data.get('profile_picture', None)
        )
        return user