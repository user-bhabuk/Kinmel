#!/usr/bin/env python
"""
Test script to verify image upload functionality
"""

import os
import django
from pathlib import Path
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from shops.models import Shop, Product, ProductImage, Category
from users.models import User

def create_test_image(text="Test Image", width=400, height=400):
    """Create a test image"""
    img = Image.new('RGB', (width, height), color='lightblue')
    
    # Save to BytesIO
    img_io = BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    
    return img_io

def test_product_image_upload():
    """Test product image upload"""
    print("=== TESTING PRODUCT IMAGE UPLOAD ===")
    
    # Get a trader and shop
    trader = User.objects.filter(role='trader', is_approved=True).first()
    if not trader:
        print("❌ No approved trader found")
        return
    
    shop = trader.shops.first()
    if not shop:
        print("❌ No shop found for trader")
        return
    
    print(f"✅ Using trader: {trader.username}")
    print(f"✅ Using shop: {shop.name}")
    
    # Get a category
    category = Category.objects.first()
    if not category:
        print("❌ No category found")
        return
    
    print(f"✅ Using category: {category.name}")
    
    # Create a test product
    product = Product.objects.create(
        shop=shop,
        category=category,
        name="Test Product with Images",
        description="This is a test product to verify image upload functionality",
        price=99.99,
        sku=f"TEST{Product.objects.count() + 1}",
        stock_quantity=10
    )
    
    print(f"✅ Created product: {product.name}")
    
    # Create test images
    for i in range(3):
        # Create test image
        img_io = create_test_image(f"Test Image {i+1}", 400, 400)
        
        # Create uploaded file
        uploaded_file = SimpleUploadedFile(
            name=f'test_image_{i+1}.png',
            content=img_io.getvalue(),
            content_type='image/png'
        )
        
        # Create ProductImage
        product_image = ProductImage.objects.create(
            product=product,
            image=uploaded_file,
            alt_text=f"Test image {i+1}",
            is_primary=(i == 0),  # First image is primary
            order=i
        )
        
        print(f"✅ Created image {i+1}: {product_image.image.name}")
        
        # Verify file exists
        image_path = Path(product_image.image.path)
        if image_path.exists():
            print(f"  ✅ File exists: {image_path}")
            print(f"  ✅ File size: {image_path.stat().st_size} bytes")
            print(f"  ✅ URL: {product_image.image.url}")
        else:
            print(f"  ❌ File not found: {image_path}")
    
    # Test product image access
    print(f"\n=== TESTING PRODUCT IMAGE ACCESS ===")
    product_images = product.images.all()
    print(f"Total images for product: {product_images.count()}")
    
    for img in product_images:
        print(f"Image: {img.image.name}")
        print(f"  URL: {img.image.url}")
        print(f"  Primary: {img.is_primary}")
        print(f"  Alt text: {img.alt_text}")
        print(f"  Order: {img.order}")
    
    # Test primary image access
    primary_image = product.images.filter(is_primary=True).first()
    if primary_image:
        print(f"\n✅ Primary image: {primary_image.image.url}")
    else:
        print(f"\n❌ No primary image found")
    
    # Test first image access (as used in templates)
    first_image = product.images.first()
    if first_image:
        print(f"✅ First image: {first_image.image.url}")
    else:
        print(f"❌ No first image found")
    
    return product

def test_shop_image_upload():
    """Test shop image upload"""
    print("\n=== TESTING SHOP IMAGE UPLOAD ===")
    
    # Get a trader
    trader = User.objects.filter(role='trader', is_approved=True).first()
    if not trader:
        print("❌ No approved trader found")
        return
    
    # Create test shop with images
    logo_io = create_test_image("Shop Logo", 200, 200)
    banner_io = create_test_image("Shop Banner", 800, 200)
    
    logo_file = SimpleUploadedFile(
        name='test_shop_logo.png',
        content=logo_io.getvalue(),
        content_type='image/png'
    )
    
    banner_file = SimpleUploadedFile(
        name='test_shop_banner.png',
        content=banner_io.getvalue(),
        content_type='image/png'
    )
    
    shop = Shop.objects.create(
        owner=trader,
        name="Test Shop with Images",
        description="This is a test shop to verify image upload functionality",
        address="123 Test Street",
        phone="1234567890",
        email="test@shop.com",
        logo=logo_file,
        banner=banner_file
    )
    
    print(f"✅ Created shop: {shop.name}")
    
    if shop.logo:
        print(f"✅ Logo: {shop.logo.url}")
        logo_path = Path(shop.logo.path)
        print(f"  File exists: {logo_path.exists()}")
        if logo_path.exists():
            print(f"  File size: {logo_path.stat().st_size} bytes")
    
    if shop.banner:
        print(f"✅ Banner: {shop.banner.url}")
        banner_path = Path(shop.banner.path)
        print(f"  File exists: {banner_path.exists()}")
        if banner_path.exists():
            print(f"  File size: {banner_path.stat().st_size} bytes")
    
    return shop

def main():
    """Main function"""
    try:
        print("🧪 TESTING IMAGE UPLOAD FUNCTIONALITY")
        print("=" * 50)
        
        # Test product image upload
        product = test_product_image_upload()
        
        # Test shop image upload
        shop = test_shop_image_upload()
        
        print("\n" + "=" * 50)
        print("✅ ALL TESTS COMPLETED")
        print(f"✅ Test product created: {product.name} (ID: {product.id})")
        print(f"✅ Test shop created: {shop.name} (ID: {shop.id})")
        print("\nYou can now:")
        print(f"1. Visit the product: http://127.0.0.1:8080/product/{product.id}/")
        print(f"2. Visit the shop: http://127.0.0.1:8080/shop/{shop.id}/")
        print("3. Check if images display correctly")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
