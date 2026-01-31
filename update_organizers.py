from apps.accounts.models import User
import random

# List of random organizer names
organizer_names = [
    ("Priya", "Sharma"),
    ("Rahul", "Verma"),
    ("Anjali", "Patel"),
    ("Arjun", "Singh"),
    ("Sneha", "Kumar"),
    ("Vikram", "Reddy"),
    ("Neha", "Gupta"),
    ("Rohan", "Mehta"),
    ("Pooja", "Joshi"),
    ("Karan", "Nair"),
]

# Get all users with username starting with 'user_'
users = User.objects.filter(username__startswith='user_')

print(f"Found {users.count()} users to update")

for i, user in enumerate(users):
    # Use modulo to cycle through names if there are more users than names
    first_name, last_name = organizer_names[i % len(organizer_names)]
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    print(f"Updated {user.username} to {first_name} {last_name}")

print("\nDone! All users updated with random names.")
