from django.contrib import admin
from .models import Notification, ChatGroup, Message

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'is_read', 'timestamp')
    list_filter = ('notification_type', 'is_read', 'timestamp')
    search_fields = ('user__username', 'title', 'message')

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0

@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_type', 'created_at')
    list_filter = ('group_type',)
    inlines = [MessageInline]
