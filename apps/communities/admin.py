from django.contrib import admin
from .models import Club, Membership

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('is_active',)

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'club', 'role', 'date_joined')
    list_filter = ('club', 'role', 'date_joined')
    search_fields = ('user__username', 'club__name')
