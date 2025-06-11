from .models import CustomUser
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only= True)
    class Meta:
        model= CustomUser
        fields= ('email','password','full_name', 'bio', 'profile_picture')

    def create(self, validates_data):
        user= CustomUser.objects.create_user(
            email= validates_data['email'],
            password= validates_data['password'],
            full_name= validates_data.get('full_name', ''),
            bio= validates_data.get('bio', ''),
            profile_picture= validates_data.get('profile_picture', None)
        )
        return user

class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields= ('email','full_name', 'bio', 'profile_picture')
        read_only_fields = ('email',)