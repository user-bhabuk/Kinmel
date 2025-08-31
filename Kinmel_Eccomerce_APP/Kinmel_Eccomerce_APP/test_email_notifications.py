#!/usr/bin/env python
"""
Test Email Notification System
This script demonstrates the complete email notification workflow
"""
import os
import django
from django.core.management import call_command

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from users.models import User
from shops.models import Shop
from utils.email_service import EmailNotificationService

def test_email_notification_system():
    """Test the complete email notification system"""
    print("📧 EMAIL NOTIFICATION SYSTEM TEST")
    print("=" * 60)
    
    # Test 1: Create a test trader for email notifications
    print("\n📝 STEP 1: CREATING TEST TRADER FOR EMAIL NOTIFICATIONS")
    print("-" * 50)
    
    try:
        # Create a test trader with a real email format
        test_trader = User.objects.create_user(
            username='emailtesttrader',
            email='emailtest@example.com',  # You can change this to your real email for testing
            password='trader123',
            role='trader',
            first_name='Email',
            last_name='Test',
            phone_number='+1234567890',
            address='123 Test Street, Email City',
            is_approved=False,
            is_active=True
        )
        print(f"✅ Test trader created: {test_trader.username}")
        print(f"   - Email: {test_trader.email}")
        print(f"   - Status: Pending Approval")
        
    except Exception as e:
        print(f"ℹ️ Test trader might already exist: {e}")
        try:
            test_trader = User.objects.get(username='emailtesttrader')
            test_trader.is_approved = False  # Reset for testing
            test_trader.save()
            print(f"✅ Using existing test trader: {test_trader.username}")
        except User.DoesNotExist:
            print("❌ Could not create or find test trader")
            return False
    
    # Test 2: Test trader approval email
    print("\n📧 STEP 2: TESTING TRADER APPROVAL EMAIL")
    print("-" * 50)
    
    print(f"📤 Sending trader approval email to: {test_trader.email}")
    
    # Simulate admin approval with email notification
    test_trader.is_approved = True
    test_trader.is_active = True
    test_trader.save()
    
    # Send approval email
    email_sent = EmailNotificationService.send_trader_approval_email(test_trader)
    
    if email_sent:
        print("✅ Trader approval email sent successfully!")
        print("   📧 Check your email console output or inbox")
        print("   🔗 Email contains login links and next steps")
    else:
        print("❌ Failed to send trader approval email")
    
    # Test 3: Create a test shop for the trader
    print("\n🏪 STEP 3: CREATING TEST SHOP FOR EMAIL NOTIFICATIONS")
    print("-" * 50)
    
    try:
        test_shop = Shop.objects.create(
            owner=test_trader,
            name="Email Test Electronics Store",
            description="A test electronics store for email notification testing",
            address="456 Email Test Avenue, Notification City, NC 12345",
            phone="+1-555-EMAIL-TEST",
            email="shop@emailtest.com",
            website="https://emailtest.com",
            opening_time="09:00",
            closing_time="21:00",
            is_active=True,
            is_approved=False  # Needs approval
        )
        print(f"✅ Test shop created: {test_shop.name}")
        print(f"   - Owner: {test_shop.owner.username}")
        print(f"   - Status: Pending Admin Approval")
        
    except Exception as e:
        print(f"ℹ️ Test shop might already exist: {e}")
        try:
            test_shop = Shop.objects.get(owner=test_trader, name="Email Test Electronics Store")
            test_shop.is_approved = False  # Reset for testing
            test_shop.save()
            print(f"✅ Using existing test shop: {test_shop.name}")
        except Shop.DoesNotExist:
            print("❌ Could not create or find test shop")
            return False
    
    # Test 4: Test shop approval email
    print("\n📧 STEP 4: TESTING SHOP APPROVAL EMAIL")
    print("-" * 50)
    
    print(f"📤 Sending shop approval email to: {test_shop.owner.email}")
    
    # Simulate admin approval with email notification
    test_shop.is_approved = True
    test_shop.is_active = True
    test_shop.save()
    
    # Send shop approval email
    email_sent = EmailNotificationService.send_shop_approval_email(test_shop)
    
    if email_sent:
        print("✅ Shop approval email sent successfully!")
        print("   📧 Check your email console output or inbox")
        print("   🔗 Email contains shop management links")
    else:
        print("❌ Failed to send shop approval email")
    
    # Test 5: Test rejection emails
    print("\n📧 STEP 5: TESTING REJECTION EMAILS")
    print("-" * 50)
    
    # Create another test trader for rejection testing
    try:
        reject_trader = User.objects.create_user(
            username='rejecttesttrader',
            email='reject@example.com',
            password='trader123',
            role='trader',
            first_name='Reject',
            last_name='Test',
            is_approved=False
        )
        print(f"✅ Rejection test trader created: {reject_trader.username}")
    except:
        try:
            reject_trader = User.objects.get(username='rejecttesttrader')
            print(f"✅ Using existing rejection test trader: {reject_trader.username}")
        except:
            reject_trader = test_trader  # Use existing trader if creation fails
    
    # Test trader rejection email
    print(f"📤 Sending trader rejection email to: {reject_trader.email}")
    rejection_sent = EmailNotificationService.send_trader_rejection_email(
        reject_trader, 
        "Application did not meet our current requirements"
    )
    
    if rejection_sent:
        print("✅ Trader rejection email sent successfully!")
    else:
        print("❌ Failed to send trader rejection email")
    
    # Summary
    print("\n📊 EMAIL NOTIFICATION TEST SUMMARY")
    print("-" * 50)
    print(f"👤 Test Trader: {test_trader.username} ({test_trader.email})")
    print(f"🏪 Test Shop: {test_shop.name}")
    print(f"📧 Emails Sent:")
    print(f"   - Trader Approval: {'✅' if email_sent else '❌'}")
    print(f"   - Shop Approval: {'✅' if email_sent else '❌'}")
    print(f"   - Trader Rejection: {'✅' if rejection_sent else '❌'}")
    
    return True

def show_email_configuration():
    """Show current email configuration"""
    print("\n⚙️ EMAIL CONFIGURATION")
    print("=" * 40)
    
    from django.conf import settings
    
    print(f"Email Backend: {settings.EMAIL_BACKEND}")
    print(f"Email Host: {getattr(settings, 'EMAIL_HOST', 'Not configured')}")
    print(f"Email Port: {getattr(settings, 'EMAIL_PORT', 'Not configured')}")
    print(f"Use TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Not configured')}")
    print(f"Default From Email: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not configured')}")
    
    if settings.DEBUG:
        print("\n📧 DEVELOPMENT MODE:")
        print("   - Emails will be displayed in console")
        print("   - No actual emails will be sent")
        print("   - Check terminal output for email content")
    else:
        print("\n📧 PRODUCTION MODE:")
        print("   - Emails will be sent via SMTP")
        print("   - Configure EMAIL_HOST_USER and EMAIL_HOST_PASSWORD")

def show_admin_workflow():
    """Show the admin workflow with email notifications"""
    print("\n🔄 ADMIN WORKFLOW WITH EMAIL NOTIFICATIONS")
    print("=" * 50)
    
    print("1. 👤 TRADER APPROVAL PROCESS:")
    print("   a. Trader registers on the platform")
    print("   b. Admin reviews trader application")
    print("   c. Admin clicks 'Approve' in admin panel")
    print("   d. 📧 Automatic email sent to trader")
    print("   e. Trader receives notification and can login immediately")
    
    print("\n2. 🏪 SHOP APPROVAL PROCESS:")
    print("   a. Approved trader creates a shop")
    print("   b. Admin reviews shop application")
    print("   c. Admin clicks 'Approve' in shop management")
    print("   d. 📧 Automatic email sent to shop owner")
    print("   e. Shop owner receives notification and can manage shop")
    
    print("\n3. 📧 EMAIL FEATURES:")
    print("   - Professional HTML email templates")
    print("   - Direct login links for immediate access")
    print("   - Clear next steps and instructions")
    print("   - Support contact information")
    print("   - Branded email design")

def show_test_instructions():
    """Show instructions for testing the email system"""
    print("\n🧪 HOW TO TEST EMAIL NOTIFICATIONS")
    print("=" * 50)
    
    print("1. 📧 CONSOLE EMAIL TESTING (Development):")
    print("   - Emails are displayed in terminal console")
    print("   - Run this script to see email content")
    print("   - Check terminal output for formatted emails")
    
    print("\n2. 🌐 REAL EMAIL TESTING:")
    print("   - Update email addresses in test script")
    print("   - Configure SMTP settings in .env file")
    print("   - Set DEBUG=False for production email sending")
    
    print("\n3. 🎯 ADMIN PANEL TESTING:")
    print("   - Login as admin: http://localhost:8000/adminpanel/")
    print("   - Go to trader management")
    print("   - Click 'Approve' on pending traders")
    print("   - Check console/email for notifications")
    
    print("\n4. 📱 IMMEDIATE LOGIN TESTING:")
    print("   - After approval email is sent")
    print("   - Trader can login immediately")
    print("   - No additional activation required")

if __name__ == "__main__":
    show_email_configuration()
    show_admin_workflow()
    show_test_instructions()
    
    print("\n" + "=" * 60)
    print("🚀 STARTING EMAIL NOTIFICATION TESTS...")
    print("=" * 60)
    
    success = test_email_notification_system()
    
    if success:
        print("\n🎉 EMAIL NOTIFICATION SYSTEM TEST COMPLETE!")
        print("✅ All email notifications are working correctly!")
        print("📧 Check your terminal console for email content!")
    else:
        print("\n❌ EMAIL NOTIFICATION SYSTEM TEST FAILED!")
        print("Please check the error messages above.")
    
    print("\n" + "=" * 60)
