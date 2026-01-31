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

    # Cleanup old generic student data
    print("Cleaning up old generic student data...")
    User.objects.filter(username__startswith='student', is_staff=False).delete()


    first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan", "Diya", "Saanvi", "Ananya", "Aadhya", "Pari", "Saanvi", "Myra", "Riya", "Anvi", "Aardhya"]
    last_names = ["Sharma", "Verma", "Gupta", "Malhotra", "Bhatia", "Saxena", "Mehta", "Joshi", "Singh", "Kumar", "Patel", "Reddy", "Nair", "Iyer", "Rao"]

    # Create 15 dummy students
    for i in range(1, 16):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        username = f"{first_name.lower()}.{last_name.lower()}{i}"
        email = f"{username}@example.com"
        password = "password123"
        
        user, created = User.objects.get_or_create(username=username, defaults={
            'email': email,
            'role': 'STUDENT',
            'first_name': first_name,
            'last_name': last_name,
            'department': random.choice(["Computer Science", "Electronics", "Mechanical", "Civil", "IT"]),
            'year': random.randint(1, 4)
        })
        
        if created:
            user.set_password(password)
            user.save()
            print(f"Created user: {first_name} {last_name} ({username})")
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
