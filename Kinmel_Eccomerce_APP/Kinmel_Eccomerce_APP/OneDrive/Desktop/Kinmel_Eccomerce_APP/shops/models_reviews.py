"""
Review and Rating models for products and shops
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class ProductReview(models.Model):
    """Customer reviews for products"""
    product = models.ForeignKey('shops.Product', on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='product_reviews'
    )
    
    # Review content
    title = models.CharField(max_length=200)
    comment = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    
    # Review metadata
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    helpful_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['product', 'customer']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer.username} - {self.product.name} ({self.rating}★)"
    
    @property
    def star_display(self):
        """Return star display for template"""
        return '★' * self.rating + '☆' * (5 - self.rating)


class ReviewHelpful(models.Model):
    """Track which users found reviews helpful"""
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE, related_name='helpful_votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['review', 'user']


class ShopReview(models.Model):
    """Customer reviews for shops"""
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='shop_reviews'
    )
    
    # Review content
    title = models.CharField(max_length=200)
    comment = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    
    # Review categories
    product_quality_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Product quality rating"
    )
    shipping_speed_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Shipping speed rating"
    )
    customer_service_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Customer service rating"
    )
    
    # Review metadata
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['shop', 'customer']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer.username} - {self.shop.name} ({self.rating}★)"


class ReviewImage(models.Model):
    """Images attached to product reviews"""
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='review_images/')
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.review}"


class ReviewResponse(models.Model):
    """Trader responses to product reviews"""
    review = models.OneToOneField(ProductReview, on_delete=models.CASCADE, related_name='response')
    trader = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='review_responses'
    )
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Response to {self.review}"


class ReviewReport(models.Model):
    """Reports for inappropriate reviews"""
    REPORT_REASONS = [
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate Content'),
        ('fake', 'Fake Review'),
        ('offensive', 'Offensive Language'),
        ('other', 'Other'),
    ]
    
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    description = models.TextField(blank=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['review', 'reporter']
    
    def __str__(self):
        return f"Report: {self.review} - {self.reason}"
