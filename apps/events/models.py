from django.db import models
from django.conf import settings

class Event(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        UPCOMING = "UPCOMING", "Upcoming"
        COMPLETED = "COMPLETED", "Completed"
        REJECTED = "REJECTED", "Rejected"
        DRAFT = "DRAFT", "Draft"

    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events', null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    venue = models.ForeignKey('resources.Resource', on_delete=models.SET_NULL, null=True, related_name='events')
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    
    # New Fields
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    collaborating_clubs = models.ManyToManyField('communities.Club', related_name='collaborations', blank=True)
    is_published = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Participant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    attendance_status = models.BooleanField(default=False)
    roll_no = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

class Expense(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - ${self.amount} ({self.event.title})"

class CollaboratorRole(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='collaborator_roles')
    club = models.ForeignKey('communities.Club', on_delete=models.CASCADE)
    responsibility = models.CharField(max_length=200, help_text="e.g., Marketing, Logistics")
    
    class Meta:
        unique_together = ('event', 'club', 'responsibility')

    def __str__(self):
        return f"{self.club.name} - {self.responsibility} ({self.event.title})"
