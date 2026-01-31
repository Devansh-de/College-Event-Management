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
    events = Event.objects.all()
    
    if not events.exists():
        print("No events found. Please run populate_data.py first.")
        return

    # Create 15 dummy students
    for i in range(1, 16):
        username = f"student{i}"
        email = f"student{i}@example.com"
        password = "password123"
        
        user, created = User.objects.get_or_create(username=username, defaults={
            'email': email,
            'role': 'STUDENT',
            'first_name': f"Student",
            'last_name': f"{i}",
            'department': "Computer Science",
            'year': 2
        })
        
        if created:
            user.set_password(password)
            user.save()
            print(f"Created user: {username}")
        else:
            print(f"User exists: {username}")

        # Register for random events
        # Register for at least 2 events each
        selected_events = random.sample(list(events), k=min(len(events), 3))
        
        for event in selected_events:
            participant, p_created = Participant.objects.get_or_create(
                user=user,
                event=event,
                defaults={'roll_no': f"CS{2024000+i}"}
            )
            if p_created:
                print(f"Registered {username} for {event.title}")

    print("Participant population complete.")

if __name__ == '__main__':
    populate_participants()
