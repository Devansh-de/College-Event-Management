import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.events.models import Event, Participant
from apps.resources.models import Resource
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with dummy data for demo purposes'

    def handle(self, *args, **options):
        self.stdout.write('Populating database...')

        # 1. Create Users
        roles = [User.Role.ADMIN, User.Role.ORGANIZER, User.Role.STUDENT]
        first_names = [
            "Aarav", "Ananya", "Ayaan", "Isha", "Vihaan", "Saanvi", "Aditya", "Myra", "Sai", "Aadhya",
            "Ishaan", "Zoya", "Arjun", "Kavya", "Rohan", "Siddharth", "Kiara", "Aryan", "Diya", "Kabir",
            "Anika", "Vivaan", "Navya", "Reyansh", "Ishani", "Atharv", "Prisha", "Advait", "Riya", "Dhruv"
        ]
        last_names = [
            "Sharma", "Verma", "Gupta", "Malhotra", "Kapoor", "Singh", "Patel", "Reddy", "Iyer", "Nair",
            "Joshi", "Chopra", "Aggarwal", "Mehta", "Bhasin", "Trivedi", "Pandey", "Chatterjee", "Mukherjee", "Desai",
            "Kulkarni", "Kaur", "Bose", "Ghosh", "Sinha", "Prasad", "Naidu", "Shetty", "Rao", "Menon"
        ]
        
        # Create unique combinations and shuffle them
        name_combinations = [(f, l) for f in first_names for l in last_names]
        random.shuffle(name_combinations)
        
        users = []
        for i in range(40): # Increased to 40 users for a diverse list
            username = f'user_{i}'
            first_name, last_name = name_combinations[i % len(name_combinations)]
            email = f"{first_name.lower()}.{last_name.lower()}@example.com"
            
            if not User.objects.filter(username=username).exists():
                role = random.choice(roles)
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='password123',
                    role=role,
                    first_name=first_name,
                    last_name=last_name
                )
                users.append(user)
            else:
                user = User.objects.get(username=username)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()
                users.append(user)

        # 2. Create Venues
        venue_names = ['Main Auditorium', 'CS Lab 1', 'Conference Room A', 'Sports Complex', 'Library Hall']
        venues = []
        for name in venue_names:
            venue, created = Resource.objects.get_or_create(
                name=name,
                defaults={
                    'resource_type': random.choice(['ROOM', 'LAB']),
                    'capacity': random.randint(20, 500),
                    'availability': True,
                    'description': f'A beautiful {name} for campus events.'
                }
            )
            venues.append(venue)

        # 3. Create Events
        event_titles = [
            'Tech Hackathon 2026', 'Cultural Night', 'Career Fair', 
            'Guest Lecture: AI Ethics', 'Sports Meet', 'Music Concert',
            'Alumni Meetup', 'Yoga Workshop', 'Coding Contest', 'Art Exhibition'
        ]
        
        organizers = [u for u in users if u.role == User.Role.ORGANIZER or u.role == User.Role.ADMIN]
        if not organizers:
            organizers = [users[0]]

        events = []
        for i, title in enumerate(event_titles):
            days_offset = random.randint(-30, 60)
            start_time = timezone.now() + timedelta(days=days_offset)
            end_time = start_time + timedelta(hours=3)
            
            status = 'UPCOMING' if days_offset > 0 else 'COMPLETED'
            if random.random() < 0.2:
                status = 'PENDING'

            event, created = Event.objects.get_or_create(
                title=title,
                defaults={
                    'description': f'Description for {title}. Join us for an amazing experience!',
                    'start_time': start_time,
                    'end_time': end_time,
                    'organizer': random.choice(organizers),
                    'venue': random.choice(venues),
                    'status': status
                }
            )
            events.append(event)

        # 4. Create Participants
        students = [u for u in users if u.role == User.Role.STUDENT]
        if students:
            random.shuffle(students)
            # Clear existing participations for these students to ensure no repeats in the final list
            Participant.objects.filter(user__in=students).delete()
            
            # Distribute students across events, each student in at most ONE event
            num_events = len(events)
            for i, student in enumerate(students):
                event = events[i % num_events]
                Participant.objects.create(
                    user=student,
                    event=event,
                    roll_no=f'BT{random.randint(1000, 9999)}',
                    attendance_status=random.choice([True, False]) if event.status == 'COMPLETED' else False
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated database with dummy data!'))
