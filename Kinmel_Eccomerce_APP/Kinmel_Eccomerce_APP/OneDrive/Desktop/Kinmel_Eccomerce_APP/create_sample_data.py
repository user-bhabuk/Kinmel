#!/usr/bin/env python
import os
import sys
import django
from decimal import Decimal

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

# Setup Django
django.setup()

from users.models import User, TraderProfile, CustomerProfile
from shops.models import Shop, Category, Product, ProductImage
from django.contrib.auth.hashers import make_password

def create_sample_data():
    print("Creating sample data...")
    
    # Create categories
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
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description'], 'is_active': True}
        )
        categories.append(category)
        if created:
            print(f"Created category: {category.name}")
    
    # Create sample customers
    customers_data = [
        {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
        {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
        {'username': 'mike_wilson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Wilson'},
    ]
    
    customers = []
    for cust_data in customers_data:
        customer, created = User.objects.get_or_create(
            username=cust_data['username'],
            defaults={
                'email': cust_data['email'],
                'first_name': cust_data['first_name'],
                'last_name': cust_data['last_name'],
                'role': 'customer',
                'is_approved': True,
                'password': make_password('password123')
            }
        )
        if created:
            CustomerProfile.objects.create(user=customer)
            customers.append(customer)
            print(f"Created customer: {customer.username}")
    
    # Create sample traders
    traders_data = [
        {
            'username': 'tech_trader',
            'email': 'tech@example.com',
            'first_name': 'Tech',
            'last_name': 'Trader',
            'business_name': 'Tech Solutions Inc',
            'business_email': 'business@techsolutions.com',
            'business_phone': '+1234567890',
            'business_address': '123 Tech Street, Silicon Valley, CA'
        },
        {
            'username': 'fashion_store',
            'email': 'fashion@example.com',
            'first_name': 'Fashion',
            'last_name': 'Store',
            'business_name': 'Fashion Forward LLC',
            'business_email': 'info@fashionforward.com',
            'business_phone': '+1234567891',
            'business_address': '456 Fashion Ave, New York, NY'
        },
    ]
    
    traders = []
    for trader_data in traders_data:
        trader, created = User.objects.get_or_create(
            username=trader_data['username'],
            defaults={
                'email': trader_data['email'],
                'first_name': trader_data['first_name'],
                'last_name': trader_data['last_name'],
                'role': 'trader',
                'is_approved': True,
                'password': make_password('password123')
            }
        )
        if created:
            TraderProfile.objects.create(
                user=trader,
                business_name=trader_data['business_name'],
                business_email=trader_data['business_email'],
                business_phone=trader_data['business_phone'],
                business_address=trader_data['business_address']
            )
            traders.append(trader)
            print(f"Created trader: {trader.username}")
    
    # Create sample shops
    if traders:
        shops_data = [
            {
                'trader': traders[0] if len(traders) > 0 else None,
                'name': 'Tech Solutions Store',
                'description': 'Your one-stop shop for all tech needs',
                'address': '123 Tech Street, Silicon Valley, CA',
                'phone': '+1234567890',
                'email': 'store@techsolutions.com'
            },
            {
                'trader': traders[1] if len(traders) > 1 else traders[0],
                'name': 'Fashion Forward Boutique',
                'description': 'Latest fashion trends and styles',
                'address': '456 Fashion Ave, New York, NY',
                'phone': '+1234567891',
                'email': 'boutique@fashionforward.com'
            },
        ]
        
        shops = []
        for shop_data in shops_data:
            if shop_data['trader']:
                shop, created = Shop.objects.get_or_create(
                    name=shop_data['name'],
                    owner=shop_data['trader'],
                    defaults={
                        'description': shop_data['description'],
                        'address': shop_data['address'],
                        'phone': shop_data['phone'],
                        'email': shop_data['email'],
                        'is_active': True,
                        'is_approved': True
                    }
                )
                if created:
                    shops.append(shop)
                    print(f"Created shop: {shop.name}")
        
        # Create sample products
        if shops and categories:
            products_data = [
                {
                    'shop': shops[0] if len(shops) > 0 else None,
                    'category': categories[0],  # Electronics
                    'name': 'Smartphone Pro Max',
                    'description': 'Latest smartphone with advanced features',
                    'price': Decimal('999.99'),
                    'original_price': Decimal('1199.99'),
                    'sku': 'PHONE-001',
                    'stock_quantity': 50,
                    'is_featured': True
                },
                {
                    'shop': shops[0] if len(shops) > 0 else None,
                    'category': categories[0],  # Electronics
                    'name': 'Wireless Headphones',
                    'description': 'High-quality wireless headphones with noise cancellation',
                    'price': Decimal('199.99'),
                    'sku': 'HEAD-001',
                    'stock_quantity': 100,
                    'is_featured': True
                },
                {
                    'shop': shops[1] if len(shops) > 1 else shops[0],
                    'category': categories[1],  # Clothing
                    'name': 'Designer T-Shirt',
                    'description': 'Premium cotton t-shirt with unique design',
                    'price': Decimal('49.99'),
                    'sku': 'SHIRT-001',
                    'stock_quantity': 200,
                    'is_featured': True
                },
                {
                    'shop': shops[1] if len(shops) > 1 else shops[0],
                    'category': categories[1],  # Clothing
                    'name': 'Denim Jeans',
                    'description': 'Classic denim jeans with modern fit',
                    'price': Decimal('79.99'),
                    'original_price': Decimal('99.99'),
                    'sku': 'JEANS-001',
                    'stock_quantity': 150
                },
            ]
            
            for prod_data in products_data:
                if prod_data['shop']:
                    product, created = Product.objects.get_or_create(
                        sku=prod_data['sku'],
                        defaults=prod_data
                    )
                    if created:
                        print(f"Created product: {product.name}")
    
    print("Sample data creation completed!")

if __name__ == '__main__':
    create_sample_data()
