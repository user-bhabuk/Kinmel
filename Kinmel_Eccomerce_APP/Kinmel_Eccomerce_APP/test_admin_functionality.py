#!/usr/bin/env python
"""
Test script to verify all admin panel functionality works correctly
"""
import os
import django
import requests
from django.test import Client
from django.contrib.auth import authenticate

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from users.models import User
from shops.models import Shop, Category, Product
from orders.models import Order

def test_admin_functionality():
    """Test all admin panel functionality"""
    print("🔧 TESTING ADMIN PANEL FUNCTIONALITY")
    print("=" * 50)
    
    # Test 1: Check if admin user exists and can authenticate
    print("\n1. Testing Admin Authentication...")
    try:
        admin_user = User.objects.get(username='admin')
        print(f"✅ Admin user found: {admin_user.username} (Role: {admin_user.role})")
        
        # Test authentication
        auth_user = authenticate(username='admin', password='admin123')
        if auth_user:
            print("✅ Admin authentication successful")
        else:
            print("❌ Admin authentication failed")
    except User.DoesNotExist:
        print("❌ Admin user not found")
        return False
    
    # Test 2: Check trader management
    print("\n2. Testing Trader Management...")
    traders = User.objects.filter(role='trader')
    print(f"✅ Found {traders.count()} traders in database")
    
    pending_traders = User.objects.filter(role='trader', is_approved=False)
    print(f"✅ Found {pending_traders.count()} pending trader approvals")
    
    # Test 3: Check shop management
    print("\n3. Testing Shop Management...")
    shops = Shop.objects.all()
    print(f"✅ Found {shops.count()} shops in database")
    
    # Test 4: Check order management
    print("\n4. Testing Order Management...")
    orders = Order.objects.all()
    print(f"✅ Found {orders.count()} orders in database")
    
    # Test 5: Test URL patterns
    print("\n5. Testing URL Patterns...")
    client = Client()
    
    # Test main admin panel (should redirect to login)
    response = client.get('/adminpanel/')
    if response.status_code == 302:
        print("✅ Admin panel URL working (redirects to login)")
    else:
        print(f"❌ Admin panel URL issue: {response.status_code}")
    
    # Test trader management URL (should redirect to login)
    response = client.get('/adminpanel/traders/')
    if response.status_code == 302:
        print("✅ Trader management URL working (redirects to login)")
    else:
        print(f"❌ Trader management URL issue: {response.status_code}")
    
    # Test with admin login
    login_success = client.login(username='admin', password='admin123')
    if login_success:
        print("✅ Admin login successful")
        
        # Test admin dashboard access
        response = client.get('/adminpanel/')
        if response.status_code == 200:
            print("✅ Admin dashboard accessible")
        else:
            print(f"❌ Admin dashboard issue: {response.status_code}")
        
        # Test trader management access
        response = client.get('/adminpanel/traders/')
        if response.status_code == 200:
            print("✅ Trader management accessible")
        else:
            print(f"❌ Trader management issue: {response.status_code}")
            
        # Test other admin pages
        admin_pages = [
            '/adminpanel/users/',
            '/adminpanel/shops/',
            '/adminpanel/orders/',
            '/adminpanel/reports/'
        ]
        
        for page in admin_pages:
            response = client.get(page)
            if response.status_code == 200:
                print(f"✅ {page} accessible")
            else:
                print(f"❌ {page} issue: {response.status_code}")
    else:
        print("❌ Admin login failed")
    
    print("\n6. Testing Database Models...")
    
    # Test User model
    try:
        user_count = User.objects.count()
        print(f"✅ User model working - {user_count} users")
    except Exception as e:
        print(f"❌ User model issue: {e}")
    
    # Test Shop model
    try:
        shop_count = Shop.objects.count()
        print(f"✅ Shop model working - {shop_count} shops")
    except Exception as e:
        print(f"❌ Shop model issue: {e}")
    
    # Test Category model
    try:
        category_count = Category.objects.count()
        print(f"✅ Category model working - {category_count} categories")
    except Exception as e:
        print(f"❌ Category model issue: {e}")
    
    # Test Product model
    try:
        product_count = Product.objects.count()
        print(f"✅ Product model working - {product_count} products")
    except Exception as e:
        print(f"❌ Product model issue: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 ADMIN FUNCTIONALITY TEST COMPLETE!")
    print("=" * 50)
    
    return True

def create_sample_data():
    """Create some sample data for testing"""
    print("\n📊 CREATING SAMPLE DATA...")
    
    # Create categories
    try:
        electronics, created = Category.objects.get_or_create(
            name='Electronics',
            defaults={'description': 'Electronic devices and gadgets'}
        )
        if created:
            print("✅ Electronics category created")
        
        clothing, created = Category.objects.get_or_create(
            name='Clothing',
            defaults={'description': 'Fashion and apparel'}
        )
        if created:
            print("✅ Clothing category created")
            
    except Exception as e:
        print(f"❌ Error creating categories: {e}")
    
    # Create a shop for the test trader
    try:
        trader = User.objects.get(username='testtrader')
        shop, created = Shop.objects.get_or_create(
            owner=trader,
            name='Test Electronics Store',
            defaults={
                'description': 'A test electronics store',
                'address': '123 Test Street, Test City',
                'phone': '+1234567890',
                'email': 'shop@test.com'
            }
        )
        if created:
            print("✅ Test shop created")
    except Exception as e:
        print(f"❌ Error creating shop: {e}")

if __name__ == "__main__":
    create_sample_data()
    test_admin_functionality()
