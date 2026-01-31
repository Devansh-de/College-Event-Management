from django.db import models
from django.conf import settings

class Club(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='club_logos/', blank=True, null=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Membership(models.Model):
    class Role(models.TextChoices):
        MEMBER = "MEMBER", "Member"
        EXECUTIVE = "EXECUTIVE", "Executive"
        HEAD = "HEAD", "Head/President"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='club_memberships')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    date_joined = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'club')

    def __str__(self):
        return f"{self.user.username} - {self.club.name} ({self.role})"
