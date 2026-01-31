from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'start_time', 'venue']
    list_filter = ['status', 'start_time']
    search_fields = ['title']

from .models import Participant
@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'attendance_status']
    list_filter = ['attendance_status', 'event']
