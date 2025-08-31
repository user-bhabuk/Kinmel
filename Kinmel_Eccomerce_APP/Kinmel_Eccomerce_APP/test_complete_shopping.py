#!/usr/bin/env python
"""
Complete Shopping Test - Simulate Real User Experience
This script tests the complete shopping flow from login to purchase
"""
import os
import django
import requests
from django.test import Client
from django.urls import reverse

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from users.models import User
from shops.models import Product
from orders.models import Cart, CartItem, Order

def test_complete_shopping_flow():
    """Test complete shopping flow with real HTTP requests"""
    print("🛒 TESTING COMPLETE SHOPPING FLOW")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000"
    
    # Step 1: Get customer account
    try:
        customer = User.objects.get(username='testcustomer')
        print(f"✅ Found customer: {customer.username}")
        print(f"   Role: {customer.role}")
        print(f"   Active: {customer.is_active}")
    except User.DoesNotExist:
        print("❌ Customer not found")
        return False
    
    # Step 2: Get a product to test with
    try:
        product = Product.objects.filter(is_active=True, stock_quantity__gt=0).first()
        if not product:
            print("❌ No products available")
            return False
        
        print(f"✅ Found product: {product.name}")
        print(f"   Price: ${product.price}")
        print(f"   Stock: {product.stock_quantity}")
        print(f"   Shop: {product.shop.name}")
    except Exception as e:
        print(f"❌ Error finding product: {e}")
        return False
    
    # Step 3: Test with Django test client
    client = Client()
    
    print(f"\n🔐 STEP 1: Testing Login")
    print("-" * 40)
    
    # Get login page first
    login_response = client.get('/users/login/')
    print(f"   Login page status: {login_response.status_code}")
    
    # Login
    login_data = {
        'username': 'testcustomer',
        'password': 'customer123'
    }
    
    login_response = client.post('/users/login/', login_data)
    print(f"   Login POST status: {login_response.status_code}")
    
    if login_response.status_code == 302:  # Redirect after successful login
        print("   ✅ Login successful")
    else:
        print("   ❌ Login failed")
        print(f"   Response: {login_response.content[:200]}")
        return False
    
    print(f"\n📦 STEP 2: Testing Product Page")
    print("-" * 40)
    
    # Get product detail page
    product_response = client.get(f'/shops/product/{product.id}/')
    print(f"   Product page status: {product_response.status_code}")
    
    if product_response.status_code == 200:
        print("   ✅ Product page accessible")
    else:
        print("   ❌ Product page failed")
        return False
    
    print(f"\n🛒 STEP 3: Testing Add to Cart")
    print("-" * 40)
    
    # Clear any existing cart
    try:
        existing_cart = Cart.objects.get(customer=customer)
        existing_cart.items.all().delete()
        print("   🧹 Cleared existing cart")
    except Cart.DoesNotExist:
        print("   📝 No existing cart")
    
    # Test add to cart
    cart_data = {
        'quantity': 2
    }
    
    cart_response = client.post(f'/orders/cart/add/{product.id}/', cart_data)
    print(f"   Add to cart status: {cart_response.status_code}")
    
    if cart_response.status_code == 200:
        try:
            response_data = cart_response.json()
            if response_data.get('success'):
                print("   ✅ Add to cart successful")
                print(f"   Message: {response_data.get('message')}")
                print(f"   Cart count: {response_data.get('cart_count')}")
            else:
                print(f"   ❌ Add to cart failed: {response_data.get('error')}")
                return False
        except Exception as e:
            print(f"   ❌ Invalid response: {e}")
            print(f"   Response: {cart_response.content}")
            return False
    else:
        print(f"   ❌ HTTP error: {cart_response.status_code}")
        print(f"   Response: {cart_response.content}")
        return False
    
    print(f"\n👁️ STEP 4: Testing Cart View")
    print("-" * 40)
    
    # View cart
    cart_view_response = client.get('/orders/cart/')
    print(f"   Cart view status: {cart_view_response.status_code}")
    
    if cart_view_response.status_code == 200:
        print("   ✅ Cart view accessible")
    else:
        print("   ❌ Cart view failed")
        return False
    
    # Check cart in database
    try:
        cart = Cart.objects.get(customer=customer)
        cart_items = cart.items.all()
        print(f"   📊 Cart items in DB: {cart_items.count()}")
        print(f"   💰 Cart total: ${cart.total_amount}")
        
        for item in cart_items:
            print(f"   - {item.product.name}: {item.quantity} x ${item.product.price}")
    except Cart.DoesNotExist:
        print("   ❌ Cart not found in database")
        return False
    
    print(f"\n💳 STEP 5: Testing Checkout")
    print("-" * 40)
    
    # Get checkout page
    checkout_response = client.get('/orders/checkout/')
    print(f"   Checkout page status: {checkout_response.status_code}")
    
    if checkout_response.status_code == 200:
        print("   ✅ Checkout page accessible")
    else:
        print("   ❌ Checkout page failed")
        return False
    
    # Submit checkout
    checkout_data = {
        'shipping_name': 'Test Customer',
        'shipping_email': customer.email,
        'shipping_phone': '+1234567890',
        'shipping_address': '123 Test Street',
        'shipping_city': 'Test City',
        'shipping_state': 'Test State',
        'shipping_postal_code': '12345',
        'payment_method': 'cash_on_delivery',
        'shipping_method': 'standard',
        'customer_notes': 'Test order from automated test'
    }
    
    checkout_submit_response = client.post('/orders/checkout/', checkout_data)
    print(f"   Checkout submit status: {checkout_submit_response.status_code}")
    
    if checkout_submit_response.status_code in [200, 302]:
        print("   ✅ Checkout submitted successfully")
        
        # Check if order was created
        try:
            order = Order.objects.filter(customer=customer).order_by('-created_at').first()
            if order:
                print(f"   📋 Order created: {order.order_number}")
                print(f"   💰 Order total: ${order.total_amount}")
                print(f"   📦 Order items: {order.items.count()}")
                print(f"   🚚 Shipping: {order.get_shipping_method_display()}")
                print(f"   💳 Payment: {order.get_payment_method_display()}")
            else:
                print("   ❌ Order not found")
                return False
        except Exception as e:
            print(f"   ❌ Error checking order: {e}")
            return False
    else:
        print(f"   ❌ Checkout failed")
        print(f"   Response: {checkout_submit_response.content[:200]}")
        return False
    
    return True

def test_with_real_http_requests():
    """Test with actual HTTP requests to the running server"""
    print(f"\n🌐 TESTING WITH REAL HTTP REQUESTS")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000"
    session = requests.Session()
    
    try:
        # Test 1: Get login page
        print("🔐 Getting login page...")
        login_page = session.get(f"{base_url}/users/login/")
        print(f"   Status: {login_page.status_code}")
        
        if login_page.status_code != 200:
            print("   ❌ Cannot access login page")
            return False
        
        # Test 2: Get products page
        print("📦 Getting products page...")
        products_page = session.get(f"{base_url}/products/")
        print(f"   Status: {products_page.status_code}")
        
        if products_page.status_code != 200:
            print("   ❌ Cannot access products page")
            return False
        
        print("   ✅ All pages accessible")
        return True
        
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to server")
        print("   Make sure the server is running on http://127.0.0.1:8000")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def show_debugging_info():
    """Show debugging information"""
    print(f"\n🔧 DEBUGGING INFORMATION")
    print("=" * 60)
    
    # Check users
    customers = User.objects.filter(role='customer', is_active=True)
    print(f"👥 Active customers: {customers.count()}")
    for customer in customers:
        print(f"   - {customer.username} ({customer.email})")
    
    # Check products
    products = Product.objects.filter(is_active=True, stock_quantity__gt=0)
    print(f"\n📦 Available products: {products.count()}")
    for product in products[:3]:
        print(f"   - {product.name}: ${product.price} (Stock: {product.stock_quantity})")
    
    # Check carts
    carts = Cart.objects.all()
    print(f"\n🛒 Existing carts: {carts.count()}")
    for cart in carts:
        print(f"   - {cart.customer.username}: {cart.items.count()} items (${cart.total_amount})")

def main():
    """Main test function"""
    try:
        # Show debugging info
        show_debugging_info()
        
        # Test with real HTTP requests first
        http_success = test_with_real_http_requests()
        
        if not http_success:
            print("\n❌ HTTP tests failed - server may not be running")
            return
        
        # Test complete shopping flow
        success = test_complete_shopping_flow()
        
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS")
        print("=" * 60)
        
        if success:
            print("🎉 ALL SHOPPING TESTS PASSED!")
            print("✅ Add to cart functionality is working")
            print("✅ Checkout process is working")
            print("✅ Order creation is working")
            
            print("\n🚀 MANUAL TESTING:")
            print("1. Go to http://127.0.0.1:8000/users/login/")
            print("2. Login with: testcustomer / customer123")
            print("3. Go to http://127.0.0.1:8000/products/")
            print("4. Click on any product")
            print("5. Click 'Add to Cart'")
            print("6. Check cart icon in navigation")
        else:
            print("❌ SHOPPING TESTS FAILED!")
            print("Check the error messages above")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
