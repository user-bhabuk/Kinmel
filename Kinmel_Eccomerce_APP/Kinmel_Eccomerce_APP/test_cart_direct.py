#!/usr/bin/env python
"""
Direct Cart Test - Test add to cart with direct database operations
This script bypasses HTTP and tests the cart functionality directly
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from users.models import User
from shops.models import Product
from orders.models import Cart, CartItem

def test_cart_directly():
    """Test cart functionality directly with database operations"""
    print("🛒 TESTING CART FUNCTIONALITY DIRECTLY")
    print("=" * 60)
    
    # Get customer
    try:
        customer = User.objects.get(username='testcustomer')
        print(f"✅ Found customer: {customer.username}")
    except User.DoesNotExist:
        print("❌ Customer not found")
        return False
    
    # Get product
    try:
        product = Product.objects.filter(is_active=True, stock_quantity__gt=0).first()
        print(f"✅ Found product: {product.name}")
    except:
        print("❌ No products found")
        return False
    
    # Clear existing cart
    try:
        existing_cart = Cart.objects.get(customer=customer)
        existing_cart.items.all().delete()
        print("🧹 Cleared existing cart")
    except Cart.DoesNotExist:
        print("📝 No existing cart")
    
    # Test 1: Create cart and add item
    print(f"\n🛒 TEST 1: Adding item to cart")
    try:
        cart, created = Cart.objects.get_or_create(customer=customer)
        print(f"   Cart created: {created}")
        
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 2}
        )
        print(f"   Item created: {item_created}")
        print(f"   Item quantity: {cart_item.quantity}")
        print(f"   Item total: ${cart_item.total_price}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Check cart totals
    print(f"\n💰 TEST 2: Checking cart totals")
    try:
        cart.refresh_from_db()
        print(f"   Cart items: {cart.items.count()}")
        print(f"   Total items: {cart.total_items}")
        print(f"   Total amount: ${cart.total_amount}")
        
        for item in cart.items.all():
            print(f"   - {item.product.name}: {item.quantity} x ${item.product.price} = ${item.total_price}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 3: Update quantity
    print(f"\n✏️ TEST 3: Updating quantity")
    try:
        cart_item.quantity = 5
        cart_item.save()
        
        cart.refresh_from_db()
        print(f"   Updated quantity: {cart_item.quantity}")
        print(f"   New total: ${cart.total_amount}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print(f"\n✅ All direct cart tests passed!")
    return True

def create_test_data():
    """Create test data if missing"""
    print(f"\n📝 CREATING TEST DATA")
    print("=" * 60)
    
    # Ensure customer exists
    customer, created = User.objects.get_or_create(
        username='testcustomer',
        defaults={
            'email': 'customer@test.com',
            'role': 'customer',
            'is_active': True,
            'first_name': 'Test',
            'last_name': 'Customer'
        }
    )
    
    if created:
        customer.set_password('customer123')
        customer.save()
        print(f"✅ Created customer: {customer.username}")
    else:
        print(f"✅ Customer exists: {customer.username}")
    
    # Check products
    products = Product.objects.filter(is_active=True, stock_quantity__gt=0)
    print(f"✅ Available products: {products.count()}")
    
    if products.count() == 0:
        print("❌ No products available for testing")
        return False
    
    return True

def show_cart_status():
    """Show current cart status for all users"""
    print(f"\n📊 CURRENT CART STATUS")
    print("=" * 60)
    
    carts = Cart.objects.all()
    print(f"Total carts: {carts.count()}")
    
    for cart in carts:
        print(f"\n👤 {cart.customer.username}:")
        print(f"   Items: {cart.items.count()}")
        print(f"   Total: ${cart.total_amount}")
        
        for item in cart.items.all():
            print(f"   - {item.product.name}: {item.quantity} x ${item.product.price}")

def main():
    """Main test function"""
    try:
        # Create test data
        if not create_test_data():
            return
        
        # Show current status
        show_cart_status()
        
        # Test cart functionality
        success = test_cart_directly()
        
        # Show final status
        show_cart_status()
        
        print("\n" + "=" * 60)
        if success:
            print("🎉 DIRECT CART TESTS PASSED!")
            print("✅ Cart model functionality is working")
            print("✅ Database operations are working")
            print("\n🔍 NEXT: Test the web interface")
            print("1. Go to http://127.0.0.1:8000/users/login/")
            print("2. Login with: testcustomer / customer123")
            print("3. Go to products and try add to cart")
            print("4. Check browser console for any errors")
        else:
            print("❌ DIRECT CART TESTS FAILED!")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
