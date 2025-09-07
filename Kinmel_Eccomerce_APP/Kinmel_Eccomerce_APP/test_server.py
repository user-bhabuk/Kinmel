#!/usr/bin/env python
"""
Test script to diagnose server issues
"""

import os
import sys
import django
from pathlib import Path

def test_django_setup():
    """Test Django setup"""
    try:
        # Set up Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
        django.setup()
        
        print("✅ Django setup successful")
        print(f"Django version: {django.get_version()}")
        
        # Test database connection
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ Database connection successful")
        
        # Test settings
        from django.conf import settings
        print(f"✅ DEBUG mode: {settings.DEBUG}")
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"✅ Database: {settings.DATABASES['default']['ENGINE']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def run_server():
    """Run the Django server"""
    try:
        from django.core.management import execute_from_command_line
        
        print("🚀 Starting Django development server...")
        print("📍 Server will be available at: http://127.0.0.1:8000")
        print("🛑 Press Ctrl+C to stop")
        
        # Run the server
        execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server failed to start: {e}")

def main():
    """Main function"""
    print("🔍 Testing Django setup...")
    
    # Change to the correct directory
    current_dir = Path(__file__).parent.absolute()
    os.chdir(current_dir)
    
    if test_django_setup():
        print("\n" + "="*50)
        run_server()
    else:
        print("❌ Cannot start server due to setup issues")

if __name__ == '__main__':
    main()
