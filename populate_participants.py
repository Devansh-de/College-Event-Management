import os
import django
import sys
import random

# Add the project directory to sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_hub.settings')
django.setup()

from apps.events.models import Event, Participant
from django.contrib.auth import get_user_model

def populate_participants():
    print("Populating participants...")
    
    User = get_user_model()
    admin_user = User.objects.filter(is_superuser=True).first()
    
    if not admin_user:
        print("No superuser found. Cannot register participants.")
        return

    events = Event.objects.all()
    if not events.exists():
        print("No events found. Please run populate_data.py first.")
        return

    # Register admin for all events
    for event in events:
        participant, created = Participant.objects.get_or_create(
            user=admin_user,
            event=event,
            defaults={'roll_no': 'ADMIN001'}
        )
        if created:
            print(f"Registered {admin_user.username} for event: {event.title}")
        else:
            print(f"User {admin_user.username} already registered for: {event.title}")

    print("Participant population complete.")

if __name__ == '__main__':
    populate_participants()
