from rest_framework import serializers
from .models import Event, RSVP
from rest_framework_simplejwt.tokens import RefreshToken

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['created_by']
        
class RSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSVP
        fields = '__all__'
        