import os
import django
import sys

# Add the project directory to sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_hub.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password, role='ADMIN')
    print(f"Superuser '{username}' created with role ADMIN.")
else:
    print(f"Superuser '{username}' already exists. Updating password and role.")
    u = User.objects.get(username=username)
    u.set_password(password)
    u.role = 'ADMIN'  # Ensure role is ADMIN
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print(f"Password and role for '{username}' updated.")
