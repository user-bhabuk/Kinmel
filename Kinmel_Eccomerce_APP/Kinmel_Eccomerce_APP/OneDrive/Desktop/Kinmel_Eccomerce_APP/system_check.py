#!/usr/bin/env python
"""
Comprehensive system check for Kinmel E-commerce application
"""

import os
import sys
import requests
import subprocess

def check_server_status():
    """Check if Django server is running"""
    try:
        response = requests.get('http://localhost:8000', timeout=5)
        if response.status_code == 200:
            print("✅ Django server is running and responding")
            return True
        else:
            print(f"⚠️ Server responding with status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        print("❌ Django server is not running")
        return False

def check_admin_access():
    """Check if admin panel is accessible"""
    try:
        response = requests.get('http://localhost:8000/admin/', timeout=5)
        if response.status_code in [200, 302]:  # 302 is redirect to login
            print("✅ Admin panel is accessible")
            return True
        else:
            print(f"⚠️ Admin panel issue: {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        print("❌ Admin panel not accessible")
        return False

def check_key_pages():
    """Check key application pages"""
    pages = {
        'Home': '/',
        'Products': '/products/',
        'Login': '/users/login/',
        'Register Customer': '/users/register/customer/',
        'Register Trader': '/users/register/trader/',
    }
    
    working_pages = 0
    for name, url in pages.items():
        try:
            response = requests.get(f'http://localhost:8000{url}', timeout=5)
            if response.status_code == 200:
                print(f"✅ {name} page working")
                working_pages += 1
            else:
                print(f"⚠️ {name} page issue: {response.status_code}")
        except requests.exceptions.RequestException:
            print(f"❌ {name} page not accessible")
    
    return working_pages, len(pages)

def check_database():
    """Check database connectivity"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
        import django
        django.setup()
        
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ Database connection working")
        
        # Check if tables exist
        from users.models import User
        user_count = User.objects.count()
        print(f"✅ Database has {user_count} users")
        
        return True
    except Exception as e:
        print(f"❌ Database issue: {e}")
        return False

def check_static_files():
    """Check if static files are being served"""
    try:
        response = requests.get('http://localhost:8000/static/css/style.css', timeout=5)
        if response.status_code == 200:
            print("✅ Static files are being served")
            return True
        else:
            print(f"⚠️ Static files issue: {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        print("❌ Static files not accessible")
        return False

def main():
    """Run comprehensive system check"""
    print("🔍 KINMEL E-COMMERCE SYSTEM CHECK")
    print("=" * 50)
    
    # Check server status
    server_running = check_server_status()
    
    if not server_running:
        print("\n❌ Server is not running. Please start it with:")
        print("   cd Kinmel_Eccomerce_APP")
        print("   venv\\Scripts\\activate")
        print("   python manage.py runserver 8000")
        return
    
    print()
    
    # Check admin access
    check_admin_access()
    
    print()
    
    # Check key pages
    working, total = check_key_pages()
    print(f"\n📊 Page Status: {working}/{total} pages working")
    
    print()
    
    # Check database
    check_database()
    
    print()
    
    # Check static files
    check_static_files()
    
    print("\n" + "=" * 50)
    
    if working == total and server_running:
        print("🎉 SYSTEM STATUS: ALL SYSTEMS OPERATIONAL!")
        print("\n📋 Quick Access:")
        print("   🌐 Application: http://localhost:8000")
        print("   👨‍💼 Admin Panel: http://localhost:8000/admin")
        print("   📦 Products: http://localhost:8000/products")
        print("   👤 Login: http://localhost:8000/users/login")
        print("\n🔑 Admin Credentials:")
        print("   Username: admin")
        print("   Password: admin123")
    else:
        print("⚠️ SYSTEM STATUS: SOME ISSUES DETECTED")
        print("   Please check the errors above and fix them.")

if __name__ == '__main__':
    main()
