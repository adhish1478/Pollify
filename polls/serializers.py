from .models import Poll, PollOption
from rest_framework import serializers

class PollOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model= PollOption
        fields= ['id', 'option_text']

class PollSerializer(serializers.ModelSerializer):
    options= PollOptionSerializer(many= True)
    class Meta:
        model= Poll
        fields= ['id','question','image','created_by','options']
        read_only_fields= ['created_by']

    def validate_options(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A poll must have at least two options.")
        option_texts= [opt['option_text'] for opt in value]
        if len(option_texts) != len(set(option_texts)):
            raise serializers.ValidationError("Poll options must be unique.")
        return value
    
    def create(self, validated_data):
        option_data = validated_data.pop('options')
        poll= Poll.objects.create(**validated_data)
        for option in option_data:
            PollOption.objects.create(poll=poll, **option)
        return poll