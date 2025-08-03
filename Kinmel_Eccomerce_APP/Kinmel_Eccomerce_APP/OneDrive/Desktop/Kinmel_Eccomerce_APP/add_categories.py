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

from shops.models import Category

def add_categories():
    print("Adding categories...")
    
    categories_data = [
        {'name': 'Electronics', 'description': 'Electronic devices, gadgets, and tech accessories'},
        {'name': 'Clothing', 'description': 'Fashion, apparel, and accessories'},
        {'name': 'Makeup', 'description': 'Cosmetics, beauty products, and makeup tools'},
        {'name': 'Skincare', 'description': 'Skincare products, treatments, and beauty care'},
        {'name': 'Medicine', 'description': 'Health products, supplements, and medical supplies'},
        {'name': 'Furniture', 'description': 'Home furniture, decor, and interior design'},
        {'name': 'Books', 'description': 'Books, educational materials, and literature'},
        {'name': 'Sports', 'description': 'Sports equipment, fitness gear, and outdoor activities'},
        {'name': 'Automotive', 'description': 'Car accessories, parts, and automotive supplies'},
        {'name': 'Jewelry', 'description': 'Jewelry, watches, and luxury accessories'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description'], 'is_active': True}
        )
        if created:
            print(f"Created category: {category.name}")
        else:
            print(f"Category already exists: {category.name}")
    
    print("Categories added successfully!")

if __name__ == '__main__':
    add_categories()
