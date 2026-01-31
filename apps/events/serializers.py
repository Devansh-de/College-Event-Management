from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.events.models import Event, Participant
from apps.resources.models import Resource

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'first_name', 'last_name')

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    organizer_name = serializers.ReadOnlyField(source='organizer.username')
    venue_name = serializers.ReadOnlyField(source='venue.name')
    
    class Meta:
        model = Event
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    event_title = serializers.ReadOnlyField(source='event.title')

    class Meta:
        model = Participant
        fields = '__all__'
