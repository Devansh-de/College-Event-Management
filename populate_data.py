import os
import django
import sys
from django.utils import timezone
from datetime import timedelta

# Add the project directory to sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_hub.settings')
django.setup()

from apps.communities.models import Club
from apps.resources.models import Resource
from apps.events.models import Event
from django.contrib.auth import get_user_model

def populate():
    print("Populating data...")
    
    User = get_user_model()
    # Get or create an admin user for organizer
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("No superuser found. Skipping event creation requiring an organizer.")
        # We can still create resources and clubs
    
    # 1. Create Resources (Venues)
    resources_data = [
        {"name": "Main Auditorium", "type": Resource.Type.ROOM, "capacity": 500, "description": "Large auditorium for major events."},
        {"name": "Seminar Hall A", "type": Resource.Type.ROOM, "capacity": 100, "description": "AV-equipped seminar hall."},
        {"name": "Computer Lab 1", "type": Resource.Type.LAB, "capacity": 50, "description": "High-performance computing lab."},
        {"name": "Sports Ground", "type": Resource.Type.ROOM, "capacity": 1000, "description": "Outdoor sports field."},
    ]

    for r_data in resources_data:
        resource, created = Resource.objects.get_or_create(name=r_data['name'], defaults=r_data)
        if created:
            print(f"Created Resource: {resource.name}")
        else:
            print(f"Resource already exists: {resource.name}")

    # 2. Create Clubs
    clubs_data = [
        {"name": "Tech Club", "description": "For technology enthusiasts and coding wizards.", "email": "tech@example.com"},
        {"name": "Cultural Club", "description": "Celebrating art, music, and dance.", "email": "culture@example.com"},
        {"name": "Sports Committee", "description": "Managing all sports events on campus.", "email": "sports@example.com"},
    ]

    for c_data in clubs_data:
        club, created = Club.objects.get_or_create(name=c_data['name'], defaults=c_data)
        if created:
            print(f"Created Club: {club.name}")
        else:
            print(f"Club already exists: {club.name}")

    # 3. Create Events (only if we have an admin user)
    if admin_user:
        # Get some resources and clubs
        auditorium = Resource.objects.get(name="Main Auditorium")
        tech_club = Club.objects.get(name="Tech Club")
        
        events_data = [
            {
                "title": "Annual Tech Hackathon",
                "description": "24-hour coding marathon to solve real-world problems.",
                "start_time": timezone.now() + timedelta(days=5),
                "end_time": timezone.now() + timedelta(days=5, hours=24),
                "organizer": admin_user,
                "status": Event.Status.UPCOMING,
                "venue": auditorium,
                "is_published": True,
                "budget": 5000.00
            },
            {
                "title": "Freshers Welcome Party",
                "description": "Welcoming the new batch of students.",
                "start_time": timezone.now() + timedelta(days=10, hours=18),
                "end_time": timezone.now() + timedelta(days=10, hours=22),
                "organizer": admin_user,
                "status": Event.Status.UPCOMING,
                "venue": auditorium,
                "is_published": True,
                "budget": 2000.00
            }
        ]

        for e_data in events_data:
            event, created = Event.objects.get_or_create(title=e_data['title'], defaults=e_data)
            if created:
                # Add a collaborating club
                event.collaborating_clubs.add(tech_club)
                print(f"Created Event: {event.title}")
            else:
                print(f"Event already exists: {event.title}")

    print("Data population complete.")

if __name__ == '__main__':
    populate()
