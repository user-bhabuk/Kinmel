#!/usr/bin/env python
"""
Complete Shop Creation Process Demo
This script demonstrates the entire process from trader registration to shop creation
"""
import os
import django
from django.contrib.auth import authenticate

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from users.models import User
from shops.models import Shop, Category, Product

def demo_complete_shop_creation_process():
    """Demonstrate the complete shop creation process"""
    print("🏪 COMPLETE SHOP CREATION PROCESS DEMO")
    print("=" * 60)
    
    # Step 1: Create a new trader (simulating registration)
    print("\n📝 STEP 1: TRADER REGISTRATION")
    print("-" * 40)
    
    try:
        # Create a new trader user
        new_trader = User.objects.create_user(
            username='newtrader',
            email='newtrader@example.com',
            password='trader123',
            role='trader',
            first_name='John',
            last_name='Smith',
            phone_number='+1234567890',
            address='123 Business Street, City, State',
            is_approved=False,  # Initially not approved
            is_active=True
        )
        print(f"✅ New trader registered: {new_trader.username}")
        print(f"   - Email: {new_trader.email}")
        print(f"   - Status: {'Approved' if new_trader.is_approved else 'Pending Approval'}")
        
    except Exception as e:
        print(f"ℹ️ Trader might already exist: {e}")
        new_trader = User.objects.get(username='newtrader')
    
    # Step 2: Admin approval process
    print("\n👑 STEP 2: ADMIN APPROVAL PROCESS")
    print("-" * 40)
    
    if not new_trader.is_approved:
        print(f"⏳ Trader {new_trader.username} is pending approval")
        print("   Admin needs to approve this trader before they can create shops")
        
        # Simulate admin approval
        admin_user = User.objects.get(username='admin')
        print(f"🔧 Admin {admin_user.username} reviewing trader application...")
        
        # Approve the trader
        new_trader.is_approved = True
        new_trader.save()
        print(f"✅ Trader {new_trader.username} has been APPROVED!")
    else:
        print(f"✅ Trader {new_trader.username} is already approved")
    
    # Step 3: Shop creation process
    print("\n🏪 STEP 3: SHOP CREATION PROCESS")
    print("-" * 40)
    
    if new_trader.is_approved:
        print(f"🎯 Trader {new_trader.username} can now create shops")
        
        # Check current shop count
        current_shops = new_trader.shops.count()
        print(f"   Current shops: {current_shops}/4 (max allowed)")
        
        if current_shops < 4:
            # Create a new shop
            try:
                new_shop = Shop.objects.create(
                    owner=new_trader,
                    name="Tech Paradise Store",
                    description="Your one-stop destination for the latest technology and gadgets. We offer high-quality electronics, accessories, and tech solutions for all your needs.",
                    address="456 Tech Avenue, Innovation District, Tech City, TC 12345",
                    phone="+1-555-TECH-123",
                    email="contact@techparadise.com",
                    website="https://techparadise.com",
                    opening_time="09:00",
                    closing_time="21:00",
                    is_active=True,
                    is_approved=False  # Needs admin approval
                )
                print(f"✅ Shop created successfully: {new_shop.name}")
                print(f"   - Owner: {new_shop.owner.username}")
                print(f"   - Address: {new_shop.address}")
                print(f"   - Status: {'Approved' if new_shop.is_approved else 'Pending Admin Approval'}")
                
            except Exception as e:
                print(f"❌ Error creating shop: {e}")
                # Try to get existing shop
                try:
                    new_shop = Shop.objects.get(owner=new_trader, name="Tech Paradise Store")
                    print(f"ℹ️ Shop already exists: {new_shop.name}")
                except Shop.DoesNotExist:
                    new_shop = None
        else:
            print("❌ Trader has reached maximum shop limit (4 shops)")
            new_shop = new_trader.shops.first()
    else:
        print("❌ Trader is not approved yet")
        new_shop = None
    
    # Step 4: Add products to the shop
    if new_shop:
        print("\n📦 STEP 4: ADDING PRODUCTS TO SHOP")
        print("-" * 40)
        
        # Ensure we have categories
        electronics_category, created = Category.objects.get_or_create(
            name='Electronics',
            defaults={'description': 'Electronic devices and gadgets'}
        )
        
        # Create sample products
        sample_products = [
            {
                'name': 'iPhone 15 Pro',
                'description': 'Latest Apple iPhone with advanced camera system and A17 Pro chip',
                'price': 999.99,
                'original_price': 1099.99,
                'stock_quantity': 50,
                'sku': 'IPHONE15PRO-001',
                'brand': 'Apple',
                'condition': 'new'
            },
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'description': 'Premium Android smartphone with S Pen and exceptional camera',
                'price': 899.99,
                'original_price': 999.99,
                'stock_quantity': 30,
                'sku': 'GALAXY-S24-ULTRA',
                'brand': 'Samsung',
                'condition': 'new'
            },
            {
                'name': 'MacBook Air M3',
                'description': 'Ultra-thin laptop with M3 chip, perfect for professionals',
                'price': 1299.99,
                'stock_quantity': 20,
                'sku': 'MACBOOK-AIR-M3',
                'brand': 'Apple',
                'condition': 'new'
            }
        ]
        
        for product_data in sample_products:
            try:
                product, created = Product.objects.get_or_create(
                    shop=new_shop,
                    sku=product_data['sku'],
                    defaults={
                        'category': electronics_category,
                        'name': product_data['name'],
                        'description': product_data['description'],
                        'price': product_data['price'],
                        'original_price': product_data.get('original_price'),
                        'stock_quantity': product_data['stock_quantity'],
                        'brand': product_data['brand'],
                        'condition': product_data['condition'],
                        'is_active': True,
                        'is_featured': True
                    }
                )
                if created:
                    print(f"✅ Product added: {product.name} - ${product.price}")
                else:
                    print(f"ℹ️ Product already exists: {product.name}")
            except Exception as e:
                print(f"❌ Error adding product {product_data['name']}: {e}")
    
    # Step 5: Summary
    print("\n📊 STEP 5: CREATION SUMMARY")
    print("-" * 40)
    
    print(f"👤 Trader: {new_trader.username}")
    print(f"   - Status: {'✅ Approved' if new_trader.is_approved else '⏳ Pending'}")
    print(f"   - Shops: {new_trader.shops.count()}/4")
    
    if new_shop:
        print(f"🏪 Shop: {new_shop.name}")
        print(f"   - Status: {'✅ Approved' if new_shop.is_approved else '⏳ Pending Admin Approval'}")
        print(f"   - Products: {new_shop.products.count()}")
        print(f"   - Address: {new_shop.address}")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Admin approves the shop (if pending)")
    print("2. Trader can add more products")
    print("3. Customers can browse and purchase")
    print("4. Orders start flowing in!")

def show_shop_creation_urls():
    """Show the URLs for shop creation process"""
    print("\n🔗 SHOP CREATION URLs")
    print("=" * 40)
    print("1. Trader Registration: http://localhost:8000/users/register/trader/")
    print("2. Trader Login: http://localhost:8000/users/login/?role=trader")
    print("3. Admin Login: http://localhost:8000/users/login/?role=admin")
    print("4. Admin Panel: http://localhost:8000/adminpanel/")
    print("5. Trader Management: http://localhost:8000/adminpanel/traders/")
    print("6. Create Shop: http://localhost:8000/shops/create/")
    print("7. Trader Dashboard: http://localhost:8000/shops/trader/dashboard/")

def show_test_credentials():
    """Show test credentials"""
    print("\n🔑 TEST CREDENTIALS")
    print("=" * 30)
    print("Admin:")
    print("  Username: admin")
    print("  Password: admin123")
    print()
    print("New Trader:")
    print("  Username: newtrader")
    print("  Password: trader123")
    print()
    print("Existing Test Trader:")
    print("  Username: testtrader")
    print("  Password: trader123")

if __name__ == "__main__":
    demo_complete_shop_creation_process()
    show_shop_creation_urls()
    show_test_credentials()
    
    print("\n" + "=" * 60)
    print("🎉 SHOP CREATION DEMO COMPLETE!")
    print("Now you can test the complete process in your browser!")
    print("=" * 60)
