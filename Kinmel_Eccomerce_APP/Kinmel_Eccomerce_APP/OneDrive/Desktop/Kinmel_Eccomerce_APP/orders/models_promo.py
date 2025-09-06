"""
Promo code and discount system models
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
import string
import random


class PromoCode(models.Model):
    """Promotional codes for discounts"""
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
        ('free_shipping', 'Free Shipping'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Percentage (0-100) or fixed amount"
    )
    
    # Usage limits
    max_uses = models.PositiveIntegerField(default=1, help_text="Maximum number of uses")
    max_uses_per_user = models.PositiveIntegerField(default=1, help_text="Max uses per user")
    current_uses = models.PositiveIntegerField(default=0)
    
    # Validity period
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    
    # Conditions
    minimum_order_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        help_text="Minimum order amount to use this code"
    )
    maximum_discount_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Maximum discount amount (for percentage discounts)"
    )
    
    # Restrictions
    applicable_categories = models.ManyToManyField(
        'shops.Category', 
        blank=True,
        help_text="Leave empty for all categories"
    )
    applicable_shops = models.ManyToManyField(
        'shops.Shop', 
        blank=True,
        help_text="Leave empty for all shops"
    )
    first_time_users_only = models.BooleanField(default=False)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_promo_codes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.get_discount_type_display()}"
    
    @classmethod
    def generate_code(cls, length=8):
        """Generate a random promo code"""
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    def is_valid(self, user=None, order_amount=None):
        """Check if promo code is valid"""
        now = timezone.now()
        
        # Check if active
        if not self.is_active:
            return False, "Promo code is not active"
        
        # Check validity period
        if now < self.valid_from:
            return False, "Promo code is not yet valid"
        
        if now > self.valid_until:
            return False, "Promo code has expired"
        
        # Check usage limits
        if self.current_uses >= self.max_uses:
            return False, "Promo code usage limit reached"
        
        # Check user-specific limits
        if user:
            user_uses = PromoCodeUsage.objects.filter(
                promo_code=self, 
                user=user
            ).count()
            
            if user_uses >= self.max_uses_per_user:
                return False, "You have already used this promo code"
            
            # Check first-time user restriction
            if self.first_time_users_only:
                from orders.models import Order
                if Order.objects.filter(customer=user, payment_status='paid').exists():
                    return False, "This promo code is for first-time users only"
        
        # Check minimum order amount
        if order_amount and order_amount < self.minimum_order_amount:
            return False, f"Minimum order amount is ${self.minimum_order_amount}"
        
        return True, "Valid"
    
    def calculate_discount(self, order_amount):
        """Calculate discount amount for given order amount"""
        if self.discount_type == 'percentage':
            discount = order_amount * (self.discount_value / 100)
            if self.maximum_discount_amount:
                discount = min(discount, self.maximum_discount_amount)
            return discount
        elif self.discount_type == 'fixed':
            return min(self.discount_value, order_amount)
        elif self.discount_type == 'free_shipping':
            return Decimal('0.00')  # Shipping discount handled separately
        
        return Decimal('0.00')
    
    def use_code(self, user, order):
        """Mark promo code as used"""
        self.current_uses += 1
        self.save()
        
        # Create usage record
        PromoCodeUsage.objects.create(
            promo_code=self,
            user=user,
            order=order,
            discount_amount=order.discount_amount
        )


class PromoCodeUsage(models.Model):
    """Track promo code usage"""
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    used_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['promo_code', 'user', 'order']
    
    def __str__(self):
        return f"{self.promo_code.code} used by {self.user.username}"


class LoyaltyProgram(models.Model):
    """Customer loyalty program"""
    customer = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='loyalty_program'
    )
    points_balance = models.PositiveIntegerField(default=0)
    total_points_earned = models.PositiveIntegerField(default=0)
    total_points_redeemed = models.PositiveIntegerField(default=0)
    tier_level = models.CharField(
        max_length=20, 
        choices=[
            ('bronze', 'Bronze'),
            ('silver', 'Silver'),
            ('gold', 'Gold'),
            ('platinum', 'Platinum'),
        ],
        default='bronze'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.customer.username} - {self.points_balance} points"
    
    def add_points(self, points, description=""):
        """Add points to customer account"""
        self.points_balance += points
        self.total_points_earned += points
        self.update_tier()
        self.save()
        
        # Create transaction record
        LoyaltyTransaction.objects.create(
            loyalty_program=self,
            transaction_type='earned',
            points=points,
            description=description
        )
    
    def redeem_points(self, points, description=""):
        """Redeem points from customer account"""
        if points > self.points_balance:
            return False, "Insufficient points"
        
        self.points_balance -= points
        self.total_points_redeemed += points
        self.save()
        
        # Create transaction record
        LoyaltyTransaction.objects.create(
            loyalty_program=self,
            transaction_type='redeemed',
            points=points,
            description=description
        )
        
        return True, "Points redeemed successfully"
    
    def update_tier(self):
        """Update customer tier based on total points earned"""
        if self.total_points_earned >= 10000:
            self.tier_level = 'platinum'
        elif self.total_points_earned >= 5000:
            self.tier_level = 'gold'
        elif self.total_points_earned >= 1000:
            self.tier_level = 'silver'
        else:
            self.tier_level = 'bronze'


class LoyaltyTransaction(models.Model):
    """Track loyalty point transactions"""
    TRANSACTION_TYPES = [
        ('earned', 'Points Earned'),
        ('redeemed', 'Points Redeemed'),
        ('expired', 'Points Expired'),
        ('bonus', 'Bonus Points'),
    ]
    
    loyalty_program = models.ForeignKey(
        LoyaltyProgram, 
        on_delete=models.CASCADE, 
        related_name='transactions'
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    points = models.IntegerField()
    description = models.CharField(max_length=200)
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.loyalty_program.customer.username} - {self.transaction_type} {self.points} points"


class Wishlist(models.Model):
    """Customer wishlist (moved from orders app)"""
    customer = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='wishlist'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Wishlist for {self.customer.username}"
    
    @property
    def total_items(self):
        return self.items.count()


class WishlistItem(models.Model):
    """Items in customer wishlist"""
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('shops.Product', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Personal notes about this item")
    
    class Meta:
        unique_together = ['wishlist', 'product']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.product.name} in {self.wishlist.customer.username}'s wishlist"
