from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        ORGANIZER = "ORGANIZER", "Organizer"
        STUDENT = "STUDENT", "Student"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.STUDENT)
    department = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    
    def is_organizer(self):
        return self.role == self.Role.ORGANIZER or self.is_staff
        
    def is_student(self):
        return self.role == self.Role.STUDENT

class OTPVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        from django.utils import timezone
        from datetime import timedelta
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"OTP for {self.user.username}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    # Could add more fields like 'clubs_joined' if using ManyToMany, but can be done in Club model
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
