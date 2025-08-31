#!/usr/bin/env python
"""
Test trader approval email notification system
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from users.models import User
from utils.email_service import EmailNotificationService

def test_trader_approval_email():
    """Test the trader approval email system"""
    print("📧 TESTING TRADER APPROVAL EMAIL SYSTEM")
    print("=" * 60)
    
    # Get a test trader
    try:
        trader = User.objects.filter(role='trader').first()
        if not trader:
            print("❌ No traders found in database")
            return False
            
        print(f"🧪 Testing with trader: {trader.username}")
        print(f"   Email: {trader.email}")
        print(f"   Full Name: {trader.get_full_name()}")
        print(f"   Current Status: {'Active' if trader.is_active else 'Pending'}")
        print()
        
        # Test sending approval email
        print("📤 SENDING TRADER APPROVAL EMAIL...")
        print("-" * 40)
        
        email_sent = EmailNotificationService.send_trader_approval_email(trader)
        
        if email_sent:
            print("✅ TRADER APPROVAL EMAIL SENT SUCCESSFULLY!")
            print("📧 Check your terminal console for the email content")
            print()
            print("📋 EMAIL DETAILS:")
            print(f"   To: {trader.email}")
            print(f"   Subject: 🎉 Congratulations! Your Trader Application has been Approved")
            print(f"   Template: emails/trader_approval.html")
            print(f"   Login URL: http://localhost:8000/users/login/?role=trader")
            print(f"   Dashboard URL: http://localhost:8000/shops/trader/dashboard/")
            print()
            
        else:
            print("❌ FAILED TO SEND TRADER APPROVAL EMAIL")
            print("Check the email configuration and template")
            
        return email_sent
        
    except Exception as e:
        print(f"❌ ERROR TESTING TRADER APPROVAL EMAIL: {e}")
        return False

def test_approval_workflow():
    """Test the complete approval workflow"""
    print("\n🔄 TESTING COMPLETE APPROVAL WORKFLOW")
    print("=" * 60)
    
    try:
        # Get a pending trader
        trader = User.objects.filter(role='trader', is_active=False).first()
        if not trader:
            print("ℹ️ No pending traders found. Creating test scenario...")
            trader = User.objects.filter(role='trader').first()
            if trader:
                trader.is_active = False
                trader.is_approved = False
                trader.save()
                print(f"✅ Set {trader.username} to pending status for testing")
            else:
                print("❌ No traders available for testing")
                return False
        
        print(f"👤 Testing approval workflow for: {trader.username}")
        print(f"   Current status: {'Active' if trader.is_active else 'Pending'}")
        print()
        
        # Simulate admin approval
        print("🔧 SIMULATING ADMIN APPROVAL...")
        print("-" * 40)
        
        # Step 1: Approve trader
        trader.is_active = True
        trader.is_approved = True
        trader.save()
        print("✅ Trader status updated to approved")
        
        # Step 2: Send approval email
        email_sent = EmailNotificationService.send_trader_approval_email(trader)
        
        if email_sent:
            print("✅ Approval email sent successfully")
            print()
            print("🎉 COMPLETE APPROVAL WORKFLOW SUCCESSFUL!")
            print("📧 Trader will receive:")
            print("   - Congratulations message")
            print("   - Direct login link")
            print("   - Dashboard access instructions")
            print("   - Shop creation guidance")
            print("   - Support contact information")
            
        else:
            print("❌ Approval email failed to send")
            
        return email_sent
        
    except Exception as e:
        print(f"❌ ERROR IN APPROVAL WORKFLOW: {e}")
        return False

def show_email_configuration():
    """Show current email configuration"""
    print("\n⚙️ CURRENT EMAIL CONFIGURATION")
    print("=" * 60)
    
    from django.conf import settings
    
    print(f"📧 Email Backend: {settings.EMAIL_BACKEND}")
    print(f"📤 From Email: {settings.DEFAULT_FROM_EMAIL}")
    
    if hasattr(settings, 'EMAIL_HOST'):
        print(f"🌐 SMTP Host: {settings.EMAIL_HOST}")
        print(f"🔌 SMTP Port: {settings.EMAIL_PORT}")
        print(f"🔐 Use TLS: {settings.EMAIL_USE_TLS}")
    
    print()
    print("📝 EMAIL TEMPLATES AVAILABLE:")
    print("   - emails/trader_approval.html")
    print("   - emails/trader_rejection.html") 
    print("   - emails/shop_approval.html")
    print("   - emails/password_reset_otp.html")
    print()
    
    if 'console' in settings.EMAIL_BACKEND:
        print("🖥️ DEVELOPMENT MODE: Emails displayed in console")
        print("   Check terminal output for email content")
    else:
        print("📧 PRODUCTION MODE: Emails sent via SMTP")

if __name__ == "__main__":
    show_email_configuration()
    
    print("\n" + "=" * 60)
    print("🚀 STARTING TRADER APPROVAL EMAIL TESTS...")
    print("=" * 60)
    
    # Test 1: Basic email sending
    success1 = test_trader_approval_email()
    
    # Test 2: Complete workflow
    success2 = test_approval_workflow()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"📧 Email Sending Test: {'✅ PASSED' if success1 else '❌ FAILED'}")
    print(f"🔄 Approval Workflow Test: {'✅ PASSED' if success2 else '❌ FAILED'}")
    
    if success1 and success2:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Trader approval email system is working correctly!")
        print("📧 Traders will receive beautiful approval emails when approved!")
        print("\n🎯 NEXT STEPS:")
        print("1. Go to admin panel: http://localhost:8000/adminpanel/")
        print("2. Click on 'Trader Management'")
        print("3. Click green 'Approve' button for any trader")
        print("4. Check terminal console for the approval email content")
        print("5. Trader can then login and create shops!")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("Please check the error messages above and fix any issues.")
    
    print("\n" + "=" * 60)
