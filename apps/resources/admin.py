from django.contrib import admin
from .models import Resource, Booking

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'resource_type', 'capacity', 'availability']
    list_filter = ['availability', 'resource_type']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['resource', 'user', 'start_time', 'end_time', 'status']
    list_filter = ['status', 'resource']
