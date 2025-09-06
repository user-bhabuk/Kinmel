"""
Email notification service for Kinmel E-Commerce
Handles all email notifications including trader approvals, shop approvals, etc.
"""
import os
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

class EmailNotificationService:
    """Service class for handling email notifications"""
    
    @staticmethod
    def get_site_url():
        """Get the site URL for email links"""
        try:
            site = Site.objects.get_current()
            return f"http://{site.domain}"
        except:
            return "http://localhost:8000"  # Fallback for development
    
    @staticmethod
    def send_trader_approval_email(trader):
        """Send email notification when trader is approved"""
        try:
            site_url = EmailNotificationService.get_site_url()
            login_url = f"{site_url}/users/login/?role=trader"
            dashboard_url = f"{site_url}/shops/trader/dashboard/"
            create_shop_url = f"{site_url}/shops/create/"
            
            context = {
                'trader': trader,
                'site_url': site_url,
                'login_url': login_url,
                'dashboard_url': dashboard_url,
                'create_shop_url': create_shop_url,
                'support_email': 'support@kinmel.com',
            }
            
            # Render HTML email template
            html_content = render_to_string('emails/trader_approval.html', context)
            text_content = strip_tags(html_content)
            
            subject = '🎉 Congratulations! Your Trader Application has been Approved - Kinmel E-Commerce'
            
            # Create email message
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[trader.email],
            )
            email.attach_alternative(html_content, "text/html")
            
            # Send email
            email.send()
            
            logger.info(f"Trader approval email sent to {trader.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send trader approval email to {trader.email}: {str(e)}")
            return False
    
    @staticmethod
    def send_trader_rejection_email(trader, reason=""):
        """Send email notification when trader is rejected"""
        try:
            site_url = EmailNotificationService.get_site_url()
            register_url = f"{site_url}/users/register/trader/"
            
            context = {
                'trader': trader,
                'reason': reason,
                'site_url': site_url,
                'register_url': register_url,
                'support_email': 'support@kinmel.com',
            }
            
            # Render HTML email template
            html_content = render_to_string('emails/trader_rejection.html', context)
            text_content = strip_tags(html_content)
            
            subject = 'Update on Your Trader Application - Kinmel E-Commerce'
            
            # Create email message
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[trader.email],
            )
            email.attach_alternative(html_content, "text/html")
            
            # Send email
            email.send()
            
            logger.info(f"Trader rejection email sent to {trader.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send trader rejection email to {trader.email}: {str(e)}")
            return False
    
    @staticmethod
    def send_shop_approval_email(shop):
        """Send email notification when shop is approved"""
        try:
            site_url = EmailNotificationService.get_site_url()
            login_url = f"{site_url}/users/login/?role=trader"
            dashboard_url = f"{site_url}/shops/trader/dashboard/"
            shop_url = f"{site_url}/shops/{shop.id}/"
            
            context = {
                'shop': shop,
                'trader': shop.owner,
                'site_url': site_url,
                'login_url': login_url,
                'dashboard_url': dashboard_url,
                'shop_url': shop_url,
                'support_email': 'support@kinmel.com',
            }
            
            # Render HTML email template
            html_content = render_to_string('emails/shop_approval.html', context)
            text_content = strip_tags(html_content)
            
            subject = f'🏪 Great News! Your Shop "{shop.name}" has been Approved - Kinmel E-Commerce'
            
            # Create email message
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[shop.owner.email],
            )
            email.attach_alternative(html_content, "text/html")
            
            # Send email
            email.send()
            
            logger.info(f"Shop approval email sent to {shop.owner.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send shop approval email to {shop.owner.email}: {str(e)}")
            return False
    
    @staticmethod
    def send_shop_rejection_email(shop, reason=""):
        """Send email notification when shop is rejected"""
        try:
            site_url = EmailNotificationService.get_site_url()
            login_url = f"{site_url}/users/login/?role=trader"
            create_shop_url = f"{site_url}/shops/create/"
            
            context = {
                'shop': shop,
                'trader': shop.owner,
                'reason': reason,
                'site_url': site_url,
                'login_url': login_url,
                'create_shop_url': create_shop_url,
                'support_email': 'support@kinmel.com',
            }
            
            # Render HTML email template
            html_content = render_to_string('emails/shop_rejection.html', context)
            text_content = strip_tags(html_content)
            
            subject = f'Update on Your Shop "{shop.name}" Application - Kinmel E-Commerce'
            
            # Create email message
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[shop.owner.email],
            )
            email.attach_alternative(html_content, "text/html")
            
            # Send email
            email.send()
            
            logger.info(f"Shop rejection email sent to {shop.owner.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send shop rejection email to {shop.owner.email}: {str(e)}")
            return False
    
    @staticmethod
    def send_welcome_email(user):
        """Send welcome email to new users"""
        try:
            site_url = EmailNotificationService.get_site_url()
            login_url = f"{site_url}/users/login/"
            
            context = {
                'user': user,
                'site_url': site_url,
                'login_url': login_url,
                'support_email': 'support@kinmel.com',
            }
            
            # Render HTML email template
            html_content = render_to_string('emails/welcome.html', context)
            text_content = strip_tags(html_content)
            
            subject = '🎉 Welcome to Kinmel E-Commerce!'
            
            # Create email message
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.attach_alternative(html_content, "text/html")
            
            # Send email
            email.send()
            
            logger.info(f"Welcome email sent to {user.email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send welcome email to {user.email}: {str(e)}")
            return False

    @staticmethod
    def send_password_reset_otp_email(user, otp_code):
        """Send OTP email for password reset"""
        try:
            site_url = EmailNotificationService.get_site_url()
            reset_url = f"{site_url}/users/reset-password/"
            login_url = f"{site_url}/users/login/"

            context = {
                'user': user,
                'otp_code': otp_code,
                'site_url': site_url,
                'reset_url': reset_url,
                'login_url': login_url,
                'support_email': 'support@kinmel.com',
                'expires_minutes': 15,
            }

            # Render HTML email template
            html_content = render_to_string('emails/password_reset_otp.html', context)
            text_content = strip_tags(html_content)

            subject = '🔐 Your Password Reset Code - Kinmel E-Commerce'

            # Create email message
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.attach_alternative(html_content, "text/html")

            # Send email
            email.send()

            logger.info(f"Password reset OTP email sent to {user.email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send password reset OTP email to {user.email}: {str(e)}")
            return False
