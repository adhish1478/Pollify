from .models import Poll, PollOption
from rest_framework import serializers
from django.utils import timezone

class PollOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model= PollOption
        fields= ['id', 'option_text']

class PollSerializer(serializers.ModelSerializer):
    options= PollOptionSerializer(many= True)
    class Meta:
        model= Poll
        fields= ['id','question','image','created_by','end_date','options']
        read_only_fields= ['created_by']

    def get_is_active(self, obj):
        return obj.is_active()

    def validate_end_date(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("End date cannot be in the past.")
        return value

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
    
    # This method is used to update the Poll end_date only with validated data.
    def update(self, instance, validated_data):
        allowed_fields = ['end_date']
        disallowed_fields= [field for field in validated_data if field not in allowed_fields]

        if disallowed_fields:
            raise serializers.ValidationError(f"Updating fields {', '.join(disallowed_fields)} is not allowed.")
        
        # Update the end_date if provided
        instance.end_date= validated_data.get('end_date', instance.end_date)
        instance.save()
        return instance
    