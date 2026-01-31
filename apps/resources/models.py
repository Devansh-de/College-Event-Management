from django.db import models
from django.conf import settings

class Resource(models.Model):
    class Type(models.TextChoices):
        ROOM = "ROOM", "Room/Hall"
        LAB = "LAB", "Laboratory"
        EQUIPMENT = "EQUIPMENT", "Equipment"

    name = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=20, choices=Type.choices, default=Type.ROOM)
    capacity = models.IntegerField(default=0)
    availability = models.BooleanField(default=True)
    auto_approve = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_resource_type_display()})"

class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"
        REJECTED = "REJECTED", "Rejected"

    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    purpose = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        # Check for overlapping bookings for the same resource
        # status__in=[self.Status.PENDING, self.Status.CONFIRMED] to block even pending ones if desired, 
        # or just CONFIRMED. Usually blocking PENDING is safer to avoid race conditions or double booking.
        overlapping_bookings = Booking.objects.filter(
            resource=self.resource,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
            status__in=[self.Status.PENDING, self.Status.CONFIRMED]
        ).exclude(pk=self.pk)

        if overlapping_bookings.exists():
            raise ValidationError("This resource is already booked for the selected time slot.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.resource.name} booked by {self.user.username}"
