#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

# Setup Django
django.setup()

from users.models import User

try:
    admin = User.objects.get(username='admin')
    admin.role = 'admin'
    admin.save()
    print(f"Admin user role updated to: {admin.role}")
except User.DoesNotExist:
    print("Admin user not found")
except Exception as e:
    print(f"Error: {e}")
