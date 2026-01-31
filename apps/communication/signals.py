from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.events.models import Event
from apps.communities.models import Club
from apps.communication.models import ChatGroup

@receiver(post_save, sender=Event)
def create_event_chat(sender, instance, created, **kwargs):
    if created:
        ChatGroup.objects.get_or_create(
            name=f"Event Team: {instance.title}",
            event=instance,
            group_type=ChatGroup.Type.GROUP
        )

@receiver(post_save, sender=Club)
def create_club_chat(sender, instance, created, **kwargs):
    if created:
        ChatGroup.objects.get_or_create(
            name=f"Club: {instance.name}",
            club=instance,
            group_type=ChatGroup.Type.GROUP
        )
