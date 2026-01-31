from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'department', 'year')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'department', 'year')}),
    )
    list_display = ['username', 'email', 'role', 'department', 'year', 'is_staff']
    list_filter = ['role', 'department', 'year']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
