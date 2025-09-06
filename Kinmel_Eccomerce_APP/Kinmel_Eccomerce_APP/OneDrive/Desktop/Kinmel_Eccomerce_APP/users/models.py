from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta
import random
import string


class User(AbstractUser):
    """Custom User model with role-based authentication"""

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('trader', 'Trader'),
        ('customer', 'Customer'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")],
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=True)  # For trader approval
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_trader(self):
        return self.role == 'trader'

    @property
    def is_customer(self):
        return self.role == 'customer'


class TraderProfile(models.Model):
    """Extended profile for traders"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trader_profile')
    business_name = models.CharField(max_length=200)
    business_license = models.CharField(max_length=100, blank=True, null=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    business_address = models.TextField()
    business_phone = models.CharField(max_length=15)
    business_email = models.EmailField()
    bank_account_number = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    violation_count = models.IntegerField(default=0)
    is_suspended = models.BooleanField(default=False)
    suspension_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.business_name} - {self.user.username}"

    @property
    def can_create_shop(self):
        """Check if trader can create more shops (max 4)"""
        return self.user.shops.count() < 4 and not self.is_suspended


class CustomerProfile(models.Model):
    """Extended profile for customers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    reward_points = models.IntegerField(default=0)
    total_orders = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    preferred_payment_method = models.CharField(max_length=50, blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Customer"

    def add_reward_points(self, points):
        """Add reward points to customer"""
        self.reward_points += points
        self.save()

    def use_reward_points(self, points):
        """Use reward points (if available)"""
        if self.reward_points >= points:
            self.reward_points -= points
            self.save()
            return True
        return False


class ViolationLog(models.Model):
    """Track trader violations"""
    VIOLATION_TYPES = [
        ('fake_product', 'Fake Product'),
        ('poor_service', 'Poor Service'),
        ('delayed_shipping', 'Delayed Shipping'),
        ('policy_violation', 'Policy Violation'),
        ('customer_complaint', 'Customer Complaint'),
        ('other', 'Other'),
    ]

    trader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='violations')
    violation_type = models.CharField(max_length=20, choices=VIOLATION_TYPES)
    description = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_violations')
    action_taken = models.TextField(blank=True, null=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Violation: {self.trader.username} - {self.get_violation_type_display()}"


class PasswordResetOTP(models.Model):
    """OTP model for password reset functionality"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_otps')
    otp_code = models.CharField(max_length=6)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=3)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Password Reset OTP'
        verbose_name_plural = 'Password Reset OTPs'

    def save(self, *args, **kwargs):
        if not self.otp_code:
            self.otp_code = self.generate_otp()
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=15)  # OTP expires in 15 minutes
        super().save(*args, **kwargs)

    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))

    def is_valid(self):
        """Check if OTP is still valid"""
        return (
            not self.is_used and
            timezone.now() < self.expires_at and
            self.attempts < self.max_attempts
        )

    def is_expired(self):
        """Check if OTP has expired"""
        return timezone.now() > self.expires_at

    def mark_as_used(self):
        """Mark OTP as used"""
        self.is_used = True
        self.save()

    def increment_attempts(self):
        """Increment attempt count"""
        self.attempts += 1
        self.save()

    @classmethod
    def create_otp_for_user(cls, user):
        """Create a new OTP for user and invalidate old ones"""
        # Invalidate all existing OTPs for this user
        cls.objects.filter(user=user, is_used=False).update(is_used=True)

        # Create new OTP
        otp = cls.objects.create(
            user=user,
            email=user.email
        )
        return otp

    def __str__(self):
        return f"OTP for {self.user.username} - {self.otp_code} ({'Valid' if self.is_valid() else 'Invalid'})"
