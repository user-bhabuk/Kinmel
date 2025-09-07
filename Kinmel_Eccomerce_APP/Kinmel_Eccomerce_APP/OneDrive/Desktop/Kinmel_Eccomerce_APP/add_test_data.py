#!/usr/bin/env python
"""
Simple script to add test data to the Kinmel E-commerce application
Run this after setting up the database and creating the admin user
"""

import os
import sys
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from users.models import User, TraderProfile, CustomerProfile
from shops.models import Category, Shop, Product
from orders.models import Order, OrderItem, Cart, CartItem
from decimal import Decimal
import random

def create_categories():
    """Create product categories"""
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
    
    print("Creating categories...")
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description'], 'is_active': True}
        )
        if created:
            print(f"✓ Created category: {category.name}")
        else:
            print(f"- Category already exists: {category.name}")

def create_test_users():
    """Create test users"""
    print("\nCreating test users...")
    
    # Create test trader
    trader, created = User.objects.get_or_create(
        username='testtrader',
        defaults={
            'email': 'trader@test.com',
            'first_name': 'John',
            'last_name': 'Trader',
            'role': 'trader',
            'is_approved': True,
            'password': make_password('password123')
        }
    )
    
    if created:
        print("✓ Created trader: testtrader")
        TraderProfile.objects.create(
            user=trader,
            business_name='Tech Solutions Store',
            business_email='business@techsolutions.com',
            business_phone='+1234567890',
            business_address='123 Business Street, Tech City, TC 12345'
        )
        print("✓ Created trader profile")
    else:
        print("- Trader already exists: testtrader")
    
    # Create test customer
    customer, created = User.objects.get_or_create(
        username='testcustomer',
        defaults={
            'email': 'customer@test.com',
            'first_name': 'Jane',
            'last_name': 'Customer',
            'role': 'customer',
            'is_approved': True,
            'password': make_password('password123')
        }
    )
    
    if created:
        print("✓ Created customer: testcustomer")
        CustomerProfile.objects.create(user=customer)
        print("✓ Created customer profile")
    else:
        print("- Customer already exists: testcustomer")
    
    return trader, customer

def create_test_shops(trader):
    """Create test shops"""
    print("\nCreating test shops...")
    
    shops_data = [
        {
            'name': 'Tech Solutions Store',
            'description': 'Your one-stop shop for all electronic devices and gadgets',
            'address': '123 Tech Street, Silicon Valley, CA 94000',
            'phone': '+1234567890',
            'email': 'store@techsolutions.com'
        },
        {
            'name': 'Fashion Forward Boutique',
            'description': 'Latest fashion trends and premium clothing for all occasions',
            'address': '456 Fashion Ave, New York, NY 10001',
            'phone': '+1234567891',
            'email': 'boutique@fashionforward.com'
        }
    ]
    
    shops = []
    for shop_data in shops_data:
        shop, created = Shop.objects.get_or_create(
            name=shop_data['name'],
            owner=trader,
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
            print(f"✓ Created shop: {shop.name}")
        else:
            print(f"- Shop already exists: {shop.name}")
        shops.append(shop)
    
    return shops

def create_test_products(shops):
    """Create test products"""
    print("\nCreating test products...")
    
    # Get categories
    electronics = Category.objects.get(name='Electronics')
    clothing = Category.objects.get(name='Clothing')
    makeup = Category.objects.get(name='Makeup')
    
    products_data = [
        # Electronics
        {
            'shop': shops[0],
            'category': electronics,
            'name': 'iPhone 15 Pro Max',
            'description': 'Latest iPhone with advanced camera system and A17 Pro chip',
            'price': Decimal('1199.99'),
            'original_price': Decimal('1299.99'),
            'sku': 'IPHONE15PM-001',
            'stock_quantity': 25,
            'is_featured': True,
            'condition': 'new',
            'brand': 'Apple'
        },
        {
            'shop': shops[0],
            'category': electronics,
            'name': 'Samsung Galaxy S24 Ultra',
            'description': 'Premium Android smartphone with S Pen and 200MP camera',
            'price': Decimal('1099.99'),
            'sku': 'GALAXY-S24U-001',
            'stock_quantity': 30,
            'is_featured': True,
            'condition': 'new',
            'brand': 'Samsung'
        },
        {
            'shop': shops[0],
            'category': electronics,
            'name': 'MacBook Air M3',
            'description': 'Ultra-thin laptop with M3 chip and all-day battery life',
            'price': Decimal('1299.99'),
            'sku': 'MBA-M3-001',
            'stock_quantity': 15,
            'condition': 'new',
            'brand': 'Apple'
        },
        # Clothing
        {
            'shop': shops[1],
            'category': clothing,
            'name': 'Premium Cotton T-Shirt',
            'description': 'Soft, comfortable cotton t-shirt in various colors',
            'price': Decimal('29.99'),
            'original_price': Decimal('39.99'),
            'sku': 'TSHIRT-COTTON-001',
            'stock_quantity': 100,
            'is_featured': True,
            'condition': 'new'
        },
        {
            'shop': shops[1],
            'category': clothing,
            'name': 'Designer Jeans',
            'description': 'Premium denim jeans with perfect fit and comfort',
            'price': Decimal('89.99'),
            'sku': 'JEANS-DESIGNER-001',
            'stock_quantity': 50,
            'condition': 'new'
        },
        # Makeup
        {
            'shop': shops[1],
            'category': makeup,
            'name': 'Professional Makeup Kit',
            'description': 'Complete makeup kit with brushes and premium cosmetics',
            'price': Decimal('149.99'),
            'sku': 'MAKEUP-KIT-001',
            'stock_quantity': 20,
            'is_featured': True,
            'condition': 'new'
        }
    ]
    
    for prod_data in products_data:
        product, created = Product.objects.get_or_create(
            sku=prod_data['sku'],
            defaults=prod_data
        )
        if created:
            print(f"✓ Created product: {product.name}")
        else:
            print(f"- Product already exists: {product.name}")


def create_sample_orders(customer, products):
    """Create sample orders for testing"""
    print("\nCreating sample orders...")

    # Create 3 sample orders
    for i in range(3):
        # Select random products
        selected_products = random.sample(list(products), random.randint(1, 3))

        # Calculate order totals
        subtotal = Decimal('0.00')
        order_items_data = []

        for product in selected_products:
            quantity = random.randint(1, 3)
            price = product.price
            total_price = price * quantity
            subtotal += total_price

            order_items_data.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'total_price': total_price
            })

        # Calculate tax and total
        tax_amount = subtotal * Decimal('0.08')  # 8% tax
        total_amount = subtotal + tax_amount

        # Create order
        order = Order.objects.create(
            customer=customer,
            order_number=f'ORD-{1000 + i}',
            status=random.choice(['pending', 'processing', 'shipped', 'completed']),
            payment_status=random.choice(['pending', 'paid']),
            subtotal=subtotal,
            tax_amount=tax_amount,
            total_amount=total_amount,
            shipping_name=customer.get_full_name(),
            shipping_email=customer.email,
            shipping_phone='+1234567890',
            shipping_address='123 Test Street',
            shipping_city='Test City',
            shipping_state='TS',
            shipping_postal_code='12345',
            shipping_country='USA'
        )

        # Create order items
        for item_data in order_items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                quantity=item_data['quantity'],
                price=item_data['price'],
                total_price=item_data['total_price']
            )

        print(f"✓ Created order: {order.order_number} (${total_amount})")

    return Order.objects.filter(customer=customer)

def main():
    """Main function to create all test data"""
    print("🚀 Creating test data for Kinmel E-commerce...")
    print("=" * 50)
    
    try:
        # Create categories
        create_categories()
        
        # Create test users
        trader, customer = create_test_users()
        
        # Create test shops
        shops = create_test_shops(trader)
        
        # Create test products
        products = create_test_products(shops)

        # Create sample orders
        create_sample_orders(customer, Product.objects.all())
        
        print("\n" + "=" * 50)
        print("✅ Test data creation completed successfully!")
        print("\n📋 Test Accounts Created:")
        print("👨‍💼 Trader Account:")
        print("   Username: testtrader")
        print("   Password: password123")
        print("   Email: trader@test.com")
        print("\n👤 Customer Account:")
        print("   Username: testcustomer") 
        print("   Password: password123")
        print("   Email: customer@test.com")
        print("\n👨‍💻 Admin Account:")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Email: admin@kinmel.com")
        print("\n🌐 Access the application at: http://localhost:8000")
        
    except Exception as e:
        print(f"\n❌ Error creating test data: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
