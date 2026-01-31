from django.db import models
from django.conf import settings

class Notification(models.Model):
    class Type(models.TextChoices):
        INFO = "INFO", "Info"
        WARNING = "WARNING", "Warning"
        SUCCESS = "SUCCESS", "Success"
        ERROR = "ERROR", "Error"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=Type.choices, default=Type.INFO)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class ChatGroup(models.Model):
    class Type(models.TextChoices):
        DIRECT = "DIRECT", "Direct Message"
        GROUP = "GROUP", "Group Chat"

    name = models.CharField(max_length=200, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_groups')
    group_type = models.CharField(max_length=20, choices=Type.choices, default=Type.DIRECT)
    
    # Context links
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, null=True, blank=True, related_name='chats')
    club = models.ForeignKey('communities.Club', on_delete=models.CASCADE, null=True, blank=True, related_name='chats')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else f"Group {self.id}"

class Message(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message by {self.sender.username} in {self.group}"
