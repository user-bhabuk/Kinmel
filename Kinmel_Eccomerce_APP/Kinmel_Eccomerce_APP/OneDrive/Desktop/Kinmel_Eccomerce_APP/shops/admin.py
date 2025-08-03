from django.contrib import admin
from .models import Shop, Category, Product, ProductImage, DiscountRequest


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'order')


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_active', 'is_approved', 'total_rating', 'created_at')
    list_filter = ('is_active', 'is_approved', 'created_at')
    search_fields = ('name', 'owner__username', 'email')
    readonly_fields = ('total_rating', 'total_reviews', 'created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('owner', 'name', 'description')
        }),
        ('Images', {
            'fields': ('logo', 'banner')
        }),
        ('Contact Information', {
            'fields': ('address', 'phone', 'email', 'website')
        }),
        ('Business Hours', {
            'fields': ('opening_time', 'closing_time')
        }),
        ('Status', {
            'fields': ('is_active', 'is_approved')
        }),
        ('Statistics', {
            'fields': ('total_rating', 'total_reviews')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'name': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'category', 'price', 'stock_quantity', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_featured', 'condition', 'category', 'shop', 'created_at')
    search_fields = ('name', 'sku', 'description', 'shop__name')
    readonly_fields = ('total_rating', 'total_reviews', 'total_sold', 'created_at', 'updated_at')
    inlines = [ProductImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('shop', 'category', 'name', 'description', 'sku')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price')
        }),
        ('Product Details', {
            'fields': ('condition', 'brand', 'model')
        }),
        ('Inventory', {
            'fields': ('stock_quantity', 'low_stock_threshold')
        }),
        ('Dimensions & Weight', {
            'fields': ('weight', 'length', 'width', 'height')
        }),
        ('Status & Features', {
            'fields': ('is_active', 'is_featured', 'is_digital')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Statistics', {
            'fields': ('total_rating', 'total_reviews', 'total_sold')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'is_primary', 'order', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('product__name', 'alt_text')


# Review admin will be added later when review models are implemented


@admin.register(DiscountRequest)
class DiscountRequestAdmin(admin.ModelAdmin):
    list_display = ('product', 'trader', 'discount_type', 'discount_value', 'status', 'created_at')
    list_filter = ('discount_type', 'status', 'created_at')
    search_fields = ('product__name', 'trader__username', 'reason')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Request Details', {
            'fields': ('trader', 'product', 'discount_type', 'discount_value', 'reason')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
        ('Review', {
            'fields': ('status', 'admin_notes', 'reviewed_by', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


# PromoCode admin will be added later when promo models are implemented
