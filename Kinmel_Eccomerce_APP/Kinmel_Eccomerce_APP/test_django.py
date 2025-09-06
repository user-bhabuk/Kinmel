#!/usr/bin/env python
"""
Test Django setup
"""

import os
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

try:
    import django
    print("✓ Django imported successfully")
    
    django.setup()
    print("✓ Django setup successful")
    
    # Test model imports
    from users.models import User
    print("✓ User model imported")
    
    from shops.models import Category, Shop, Product
    print("✓ Shop models imported")
    
    from orders.models import Order, Cart
    print("✓ Order models imported")
    
    print("\n🎉 All imports successful! Django is working correctly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
