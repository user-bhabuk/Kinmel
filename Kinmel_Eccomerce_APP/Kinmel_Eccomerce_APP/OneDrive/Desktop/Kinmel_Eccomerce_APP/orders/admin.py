from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Invoice


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('total_price',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_items', 'total_amount', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('customer__username', 'customer__email')
    readonly_fields = ('total_items', 'total_amount', 'created_at', 'updated_at')
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'customer__username', 'customer__email')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'customer', 'status', 'payment_status')
        }),
        ('Amounts', {
            'fields': ('subtotal', 'tax_amount', 'shipping_amount', 'discount_amount', 'total_amount')
        }),
        ('Shipping Information', {
            'fields': ('shipping_name', 'shipping_email', 'shipping_phone', 'shipping_address',
                      'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country')
        }),
        ('Promo & Notes', {
            'fields': ('promo_code', 'customer_notes', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'shipped_at', 'delivered_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'total_price', 'is_shipped')
    list_filter = ('is_shipped', 'shipped_at')
    search_fields = ('order__order_number', 'product__name')
    readonly_fields = ('total_price',)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'order', 'issue_date', 'due_date', 'is_paid')
    list_filter = ('is_paid', 'issue_date', 'due_date')
    search_fields = ('invoice_number', 'order__order_number')
    readonly_fields = ('invoice_number', 'issue_date')


# Wishlist admin will be added later
