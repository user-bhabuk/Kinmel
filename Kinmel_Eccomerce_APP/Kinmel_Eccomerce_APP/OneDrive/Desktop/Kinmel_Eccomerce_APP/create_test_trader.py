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

from users.models import User, TraderProfile
from shops.models import Category
from django.contrib.auth.hashers import make_password

def create_test_data():
    print("Creating test data...")
    
    # Create categories first
    categories_data = [
        {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
        {'name': 'Clothing', 'description': 'Fashion and apparel'},
        {'name': 'Makeup', 'description': 'Cosmetics and beauty products'},
        {'name': 'Skincare', 'description': 'Skincare products and treatments'},
        {'name': 'Medicine', 'description': 'Health products and supplements'},
        {'name': 'Furniture', 'description': 'Home furniture and decor'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description'], 'is_active': True}
        )
        if created:
            print(f"Created category: {category.name}")
    
    # Create test trader
    trader, created = User.objects.get_or_create(
        username='testtrader',
        defaults={
            'email': 'trader@test.com',
            'first_name': 'Test',
            'last_name': 'Trader',
            'role': 'trader',
            'is_approved': True,
            'password': make_password('password123')
        }
    )
    
    if created:
        print(f"Created trader: {trader.username}")
        
        # Create trader profile
        TraderProfile.objects.create(
            user=trader,
            business_name='Test Electronics Store',
            business_email='business@test.com',
            business_phone='+1234567890',
            business_address='123 Business Street, City, State'
        )
        print("Created trader profile")
    else:
        print("Trader already exists")
    
    # Create test customer
    customer, created = User.objects.get_or_create(
        username='testcustomer',
        defaults={
            'email': 'customer@test.com',
            'first_name': 'Test',
            'last_name': 'Customer',
            'role': 'customer',
            'is_approved': True,
            'password': make_password('password123')
        }
    )
    
    if created:
        print(f"Created customer: {customer.username}")
    else:
        print("Customer already exists")
    
    print("Test data creation completed!")
    print("\nTest Accounts:")
    print("Trader - Username: testtrader, Password: password123")
    print("Customer - Username: testcustomer, Password: password123")
    print("Admin - Username: admin, Password: admin123")

if __name__ == '__main__':
    create_test_data()
