#!/usr/bin/env python
"""
Test Add to Cart Functionality
This script tests the add to cart functionality with proper authentication
"""
import os
import django
from django.test import Client
from django.urls import reverse

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from users.models import User
from shops.models import Product
from orders.models import Cart

def test_add_to_cart():
    """Test add to cart functionality"""
    print("🛒 TESTING ADD TO CART FUNCTIONALITY")
    print("=" * 60)
    
    # Get test customer
    try:
        customer = User.objects.get(username='testcustomer')
        print(f"✅ Found customer: {customer.username}")
        print(f"   Role: {customer.role}")
        print(f"   Active: {customer.is_active}")
        print(f"   Email: {customer.email}")
    except User.DoesNotExist:
        print("❌ Test customer not found. Run create_test_customer.py first.")
        return False
    
    # Get a test product
    try:
        product = Product.objects.filter(is_active=True, stock_quantity__gt=0).first()
        if not product:
            print("❌ No active products with stock found.")
            return False
        
        print(f"✅ Found product: {product.name}")
        print(f"   Price: ${product.price}")
        print(f"   Stock: {product.stock_quantity}")
        print(f"   Shop: {product.shop.name}")
    except Exception as e:
        print(f"❌ Error finding product: {e}")
        return False
    
    # Test with Django test client
    client = Client()
    
    # Test 1: Add to cart without login (should fail)
    print(f"\n🔒 TEST 1: Add to cart without login")
    response = client.post(f'/orders/cart/add/{product.id}/', {
        'quantity': 1
    })
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print("   ✅ Correctly rejected unauthenticated user")
    else:
        print("   ❌ Should have rejected unauthenticated user")
    
    # Test 2: Login as customer
    print(f"\n👤 TEST 2: Login as customer")
    login_success = client.login(username='testcustomer', password='testpass123')
    if login_success:
        print("   ✅ Customer login successful")
    else:
        print("   ❌ Customer login failed")
        return False
    
    # Test 3: Add to cart after login (should succeed)
    print(f"\n✅ TEST 3: Add to cart after login")
    response = client.post(f'/orders/cart/add/{product.id}/', {
        'quantity': 2
    })
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            if data.get('success'):
                print("   ✅ Successfully added to cart")
                print(f"   Message: {data.get('message')}")
                print(f"   Cart count: {data.get('cart_count')}")
            else:
                print(f"   ❌ Add to cart failed: {data.get('error')}")
        except:
            print("   ❌ Invalid JSON response")
    else:
        print(f"   ❌ HTTP error: {response.status_code}")
        try:
            error_data = response.json()
            print(f"   Error: {error_data}")
        except:
            print(f"   Response content: {response.content}")
    
    # Test 4: Check cart contents
    print(f"\n📋 TEST 4: Check cart contents")
    try:
        cart = Cart.objects.get(customer=customer)
        print(f"   ✅ Cart exists")
        print(f"   Items in cart: {cart.items.count()}")
        print(f"   Total amount: ${cart.total_amount}")
        
        for item in cart.items.all():
            print(f"   - {item.product.name}: {item.quantity} x ${item.product.price} = ${item.total_price}")
            
    except Cart.DoesNotExist:
        print("   ❌ Cart not found")
    except Exception as e:
        print(f"   ❌ Error checking cart: {e}")
    
    return True

def test_user_roles():
    """Test different user roles"""
    print(f"\n👥 TESTING USER ROLES")
    print("=" * 60)
    
    # Test all user types
    for role in ['customer', 'trader', 'admin']:
        users = User.objects.filter(role=role, is_active=True)
        print(f"\n{role.upper()}S:")
        for user in users[:3]:  # Show first 3 of each role
            print(f"   {user.username} ({user.email})")
            print(f"   - Role: {user.role}")
            print(f"   - Active: {user.is_active}")
            print(f"   - Has role attr: {hasattr(user, 'role')}")

def main():
    """Main test function"""
    try:
        # Test user roles first
        test_user_roles()
        
        # Test add to cart functionality
        success = test_add_to_cart()
        
        print("\n" + "=" * 60)
        if success:
            print("🎉 ADD TO CART TESTS COMPLETED!")
            print("\n🚀 MANUAL TESTING STEPS:")
            print("1. Go to http://127.0.0.1:8000/users/login/")
            print("2. Login with:")
            print("   Username: testcustomer")
            print("   Password: testpass123")
            print("3. Go to http://127.0.0.1:8000/products/")
            print("4. Click on any product")
            print("5. Click 'Add to Cart' button")
            print("6. Check cart icon in navigation")
        else:
            print("❌ ADD TO CART TESTS FAILED!")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
