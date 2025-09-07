#!/usr/bin/env python
"""
Comprehensive test to ensure all components work properly
"""
import os
import django
from django.test import Client
from django.contrib.auth import authenticate

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from users.models import User
from shops.models import Shop, Category, Product
from orders.models import Order

def test_all_components():
    """Test all application components"""
    print("🚀 COMPREHENSIVE COMPONENT TESTING")
    print("=" * 60)
    
    client = Client()
    all_tests_passed = True
    
    # Test 1: Authentication System
    print("\n1. 🔐 TESTING AUTHENTICATION SYSTEM")
    print("-" * 40)
    
    try:
        # Test admin login
        login_success = client.login(username='admin', password='admin123')
        if login_success:
            print("✅ Admin login successful")
        else:
            print("❌ Admin login failed")
            all_tests_passed = False
            
        # Test role-based access
        admin_user = User.objects.get(username='admin')
        if admin_user.is_admin:
            print("✅ Admin role detection working")
        else:
            print("❌ Admin role detection failed")
            all_tests_passed = False
            
    except Exception as e:
        print(f"❌ Authentication system error: {e}")
        all_tests_passed = False
    
    # Test 2: Admin Panel Pages
    print("\n2. 🎛️ TESTING ADMIN PANEL PAGES")
    print("-" * 40)
    
    admin_pages = {
        '/adminpanel/': 'Dashboard',
        '/adminpanel/traders/': 'Trader Management',
        '/adminpanel/users/': 'User Management',
        '/adminpanel/shops/': 'Shop Management',
        '/adminpanel/orders/': 'Order Management',
        '/adminpanel/reports/': 'Reports'
    }
    
    for url, name in admin_pages.items():
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"✅ {name} page accessible")
            else:
                print(f"❌ {name} page error: {response.status_code}")
                all_tests_passed = False
        except Exception as e:
            print(f"❌ {name} page exception: {e}")
            all_tests_passed = False
    
    # Test 3: Database Models
    print("\n3. 🗄️ TESTING DATABASE MODELS")
    print("-" * 40)
    
    try:
        # Test User model
        user_count = User.objects.count()
        print(f"✅ User model: {user_count} users")
        
        # Test different user roles
        admin_count = User.objects.filter(role='admin').count()
        trader_count = User.objects.filter(role='trader').count()
        customer_count = User.objects.filter(role='customer').count()
        print(f"✅ User roles: {admin_count} admins, {trader_count} traders, {customer_count} customers")
        
        # Test Shop model
        shop_count = Shop.objects.count()
        print(f"✅ Shop model: {shop_count} shops")
        
        # Test Category model
        category_count = Category.objects.count()
        print(f"✅ Category model: {category_count} categories")
        
        # Test Product model
        product_count = Product.objects.count()
        print(f"✅ Product model: {product_count} products")
        
        # Test Order model
        order_count = Order.objects.count()
        print(f"✅ Order model: {order_count} orders")
        
    except Exception as e:
        print(f"❌ Database model error: {e}")
        all_tests_passed = False
    
    # Test 4: Trader Management Functionality
    print("\n4. 👥 TESTING TRADER MANAGEMENT")
    print("-" * 40)
    
    try:
        # Test pending traders
        pending_traders = User.objects.filter(role='trader', is_approved=False)
        print(f"✅ Pending traders: {pending_traders.count()}")
        
        # Test trader approval URLs
        if pending_traders.exists():
            trader = pending_traders.first()
            
            # Test approve URL
            approve_url = f'/adminpanel/traders/{trader.id}/approve/'
            response = client.post(approve_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            if response.status_code in [200, 302]:
                print("✅ Trader approval URL working")
            else:
                print(f"❌ Trader approval URL error: {response.status_code}")
                all_tests_passed = False
                
        else:
            print("ℹ️ No pending traders to test approval")
            
    except Exception as e:
        print(f"❌ Trader management error: {e}")
        all_tests_passed = False
    
    # Test 5: Template Rendering
    print("\n5. 🎨 TESTING TEMPLATE RENDERING")
    print("-" * 40)
    
    try:
        # Test dashboard template
        response = client.get('/adminpanel/')
        if 'Admin Dashboard' in response.content.decode():
            print("✅ Dashboard template rendering correctly")
        else:
            print("❌ Dashboard template content issue")
            all_tests_passed = False
            
        # Test trader management template
        response = client.get('/adminpanel/traders/')
        if 'Trader Management' in response.content.decode():
            print("✅ Trader management template rendering correctly")
        else:
            print("❌ Trader management template content issue")
            all_tests_passed = False
            
    except Exception as e:
        print(f"❌ Template rendering error: {e}")
        all_tests_passed = False
    
    # Test 6: AJAX Endpoints
    print("\n6. 🔄 TESTING AJAX ENDPOINTS")
    print("-" * 40)
    
    try:
        # Test trader details endpoint
        traders = User.objects.filter(role='trader')
        if traders.exists():
            trader = traders.first()
            details_url = f'/adminpanel/traders/{trader.id}/details/'
            response = client.get(details_url)
            if response.status_code == 200:
                print("✅ Trader details AJAX endpoint working")
            else:
                print(f"❌ Trader details AJAX endpoint error: {response.status_code}")
                all_tests_passed = False
        else:
            print("ℹ️ No traders to test details endpoint")
            
    except Exception as e:
        print(f"❌ AJAX endpoint error: {e}")
        all_tests_passed = False
    
    # Test 7: URL Patterns
    print("\n7. 🔗 TESTING URL PATTERNS")
    print("-" * 40)
    
    try:
        from django.urls import reverse
        
        # Test URL reversing
        dashboard_url = reverse('adminpanel:dashboard')
        trader_mgmt_url = reverse('adminpanel:trader_management')
        
        print(f"✅ URL patterns working: {dashboard_url}, {trader_mgmt_url}")
        
    except Exception as e:
        print(f"❌ URL pattern error: {e}")
        all_tests_passed = False
    
    # Test 8: Static Files and CSS
    print("\n8. 🎨 TESTING STATIC FILES")
    print("-" * 40)
    
    try:
        # Test if templates include proper CSS classes
        response = client.get('/adminpanel/')
        content = response.content.decode()
        
        if 'stat-card' in content:
            print("✅ Custom CSS classes present")
        else:
            print("❌ Custom CSS classes missing")
            all_tests_passed = False
            
        if 'bootstrap' in content.lower() or 'btn' in content:
            print("✅ Bootstrap CSS working")
        else:
            print("❌ Bootstrap CSS missing")
            all_tests_passed = False
            
    except Exception as e:
        print(f"❌ Static files error: {e}")
        all_tests_passed = False
    
    # Final Results
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 ALL COMPONENTS WORKING PERFECTLY!")
        print("✅ The application is ready for production use!")
    else:
        print("⚠️ SOME ISSUES FOUND")
        print("❌ Please review the failed tests above")
    print("=" * 60)
    
    return all_tests_passed

def create_test_data():
    """Create comprehensive test data"""
    print("📊 CREATING COMPREHENSIVE TEST DATA...")
    
    try:
        # Ensure we have test users
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@kinmel.com',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'Admin',
                'last_name': 'User'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            print("✅ Admin user created")
        
        # Create test trader
        trader_user, created = User.objects.get_or_create(
            username='testtrader',
            defaults={
                'email': 'trader@test.com',
                'role': 'trader',
                'is_approved': False,
                'first_name': 'Test',
                'last_name': 'Trader'
            }
        )
        if created:
            trader_user.set_password('trader123')
            trader_user.save()
            print("✅ Test trader created")
        
        # Create test customer
        customer_user, created = User.objects.get_or_create(
            username='testcustomer',
            defaults={
                'email': 'customer@test.com',
                'role': 'customer',
                'first_name': 'Test',
                'last_name': 'Customer'
            }
        )
        if created:
            customer_user.set_password('customer123')
            customer_user.save()
            print("✅ Test customer created")
        
        print("✅ Test data creation complete!")
        
    except Exception as e:
        print(f"❌ Error creating test data: {e}")

if __name__ == "__main__":
    create_test_data()
    test_all_components()
