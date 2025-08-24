"""
Email utilities for Kinmel E-commerce application
Handles all email notifications and confirmations
"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


def send_order_confirmation_email(order):
    """Send order confirmation email to customer"""
    try:
        subject = f'Order Confirmation - #{order.order_number}'
        
        # Render HTML email template
        html_content = render_to_string('emails/order_confirmation.html', {
            'order': order,
            'customer': order.customer,
            'order_items': order.items.all(),
        })
        
        # Create plain text version
        text_content = strip_tags(html_content)
        
        # Send email
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.shipping_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        logger.info(f"Order confirmation email sent for order {order.order_number}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send order confirmation email: {e}")
        return False


def send_order_status_update_email(order, old_status, new_status):
    """Send order status update email to customer"""
    try:
        subject = f'Order Update - #{order.order_number}'
        
        html_content = render_to_string('emails/order_status_update.html', {
            'order': order,
            'customer': order.customer,
            'old_status': old_status,
            'new_status': new_status,
        })
        
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.shipping_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        logger.info(f"Order status update email sent for order {order.order_number}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send order status update email: {e}")
        return False


def send_trader_approval_email(trader):
    """Send trader approval notification email"""
    try:
        subject = 'Welcome to Kinmel E-Commerce - Trader Account Approved!'
        
        html_content = render_to_string('emails/trader_approval.html', {
            'trader': trader,
        })
        
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[trader.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        logger.info(f"Trader approval email sent to {trader.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send trader approval email: {e}")
        return False


def send_shop_approval_email(shop):
    """Send shop approval notification email"""
    try:
        subject = f'Shop Approved - {shop.name}'
        
        html_content = render_to_string('emails/shop_approval.html', {
            'shop': shop,
            'trader': shop.owner,
        })
        
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[shop.owner.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        logger.info(f"Shop approval email sent for shop {shop.name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send shop approval email: {e}")
        return False


def send_low_stock_alert_email(product):
    """Send low stock alert to trader"""
    try:
        subject = f'Low Stock Alert - {product.name}'
        
        html_content = render_to_string('emails/low_stock_alert.html', {
            'product': product,
            'trader': product.shop.owner,
        })
        
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[product.shop.owner.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        logger.info(f"Low stock alert sent for product {product.name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send low stock alert: {e}")
        return False


def send_new_order_notification_email(order):
    """Send new order notification to trader"""
    try:
        # Get all traders involved in this order
        traders = set()
        for item in order.items.all():
            traders.add(item.product.shop.owner)
        
        for trader in traders:
            # Get trader's items in this order
            trader_items = order.items.filter(product__shop__owner=trader)
            
            subject = f'New Order Received - #{order.order_number}'
            
            html_content = render_to_string('emails/new_order_notification.html', {
                'order': order,
                'trader': trader,
                'trader_items': trader_items,
            })
            
            text_content = strip_tags(html_content)
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[trader.email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            logger.info(f"New order notification sent to trader {trader.email}")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to send new order notification: {e}")
        return False


def send_welcome_email(user):
    """Send welcome email to new users"""
    try:
        if user.role == 'customer':
            subject = 'Welcome to Kinmel E-Commerce!'
            template = 'emails/welcome_customer.html'
        elif user.role == 'trader':
            subject = 'Welcome to Kinmel E-Commerce - Trader Registration Received'
            template = 'emails/welcome_trader.html'
        else:
            return False
        
        html_content = render_to_string(template, {
            'user': user,
        })
        
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        logger.info(f"Welcome email sent to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send welcome email: {e}")
        return False


def send_password_reset_email(user, reset_link):
    """Send password reset email"""
    try:
        subject = 'Password Reset - Kinmel E-Commerce'
        
        html_content = render_to_string('emails/password_reset.html', {
            'user': user,
            'reset_link': reset_link,
        })
        
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        logger.info(f"Password reset email sent to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send password reset email: {e}")
        return False


def send_newsletter_email(users, subject, content):
    """Send newsletter to multiple users"""
    try:
        for user in users:
            html_content = render_to_string('emails/newsletter.html', {
                'user': user,
                'content': content,
            })
            
            text_content = strip_tags(html_content)
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
        
        logger.info(f"Newsletter sent to {len(users)} users")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send newsletter: {e}")
        return False
