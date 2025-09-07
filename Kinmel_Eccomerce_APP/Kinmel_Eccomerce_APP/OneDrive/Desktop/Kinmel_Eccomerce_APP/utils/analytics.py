"""
Analytics utilities for Kinmel E-commerce application
Provides sales analytics, reporting, and business intelligence
"""

from django.db.models import Sum, Count, Avg, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from collections import defaultdict
import json


class SalesAnalytics:
    """Sales analytics for traders and admins"""
    
    def __init__(self, user=None, shop=None):
        self.user = user
        self.shop = shop
    
    def get_sales_summary(self, days=30):
        """Get sales summary for the last N days"""
        from orders.models import Order, OrderItem
        
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        # Base queryset
        orders = Order.objects.filter(
            created_at__gte=start_date,
            payment_status='paid'
        )
        
        # Filter by shop if specified
        if self.shop:
            orders = orders.filter(items__product__shop=self.shop).distinct()
        elif self.user and self.user.is_trader:
            orders = orders.filter(items__product__shop__owner=self.user).distinct()
        
        # Calculate metrics
        total_orders = orders.count()
        total_revenue = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
        avg_order_value = orders.aggregate(Avg('total_amount'))['total_amount__avg'] or Decimal('0.00')
        
        # Get order items for this period
        order_items = OrderItem.objects.filter(order__in=orders)
        total_items_sold = order_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
        
        return {
            'period_days': days,
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'avg_order_value': float(avg_order_value),
            'total_items_sold': total_items_sold,
        }
    
    def get_daily_sales(self, days=30):
        """Get daily sales data for charts"""
        from orders.models import Order
        
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        # Base queryset
        orders = Order.objects.filter(
            created_at__date__gte=start_date,
            payment_status='paid'
        )
        
        # Filter by shop if specified
        if self.shop:
            orders = orders.filter(items__product__shop=self.shop).distinct()
        elif self.user and self.user.is_trader:
            orders = orders.filter(items__product__shop__owner=self.user).distinct()
        
        # Group by date
        daily_sales = orders.extra(
            select={'date': 'DATE(created_at)'}
        ).values('date').annotate(
            revenue=Sum('total_amount'),
            orders=Count('id')
        ).order_by('date')
        
        # Fill missing dates with zero values
        sales_dict = {item['date']: item for item in daily_sales}
        result = []
        
        current_date = start_date
        while current_date <= end_date:
            if current_date in sales_dict:
                result.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'revenue': float(sales_dict[current_date]['revenue']),
                    'orders': sales_dict[current_date]['orders']
                })
            else:
                result.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'revenue': 0.0,
                    'orders': 0
                })
            current_date += timedelta(days=1)
        
        return result
    
    def get_top_products(self, limit=10, days=30):
        """Get top-selling products"""
        from orders.models import OrderItem
        
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        # Base queryset
        order_items = OrderItem.objects.filter(
            order__created_at__gte=start_date,
            order__payment_status='paid'
        )
        
        # Filter by shop if specified
        if self.shop:
            order_items = order_items.filter(product__shop=self.shop)
        elif self.user and self.user.is_trader:
            order_items = order_items.filter(product__shop__owner=self.user)
        
        # Group by product and calculate metrics
        top_products = order_items.values(
            'product__name',
            'product__sku',
            'product__price'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('quantity') * F('price')),
            order_count=Count('order', distinct=True)
        ).order_by('-total_revenue')[:limit]
        
        return list(top_products)
    
    def get_category_performance(self, days=30):
        """Get sales performance by category"""
        from orders.models import OrderItem
        
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        # Base queryset
        order_items = OrderItem.objects.filter(
            order__created_at__gte=start_date,
            order__payment_status='paid'
        )
        
        # Filter by shop if specified
        if self.shop:
            order_items = order_items.filter(product__shop=self.shop)
        elif self.user and self.user.is_trader:
            order_items = order_items.filter(product__shop__owner=self.user)
        
        # Group by category
        category_performance = order_items.values(
            'product__category__name'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('quantity') * F('price')),
            order_count=Count('order', distinct=True)
        ).order_by('-total_revenue')
        
        return list(category_performance)
    
    def get_customer_analytics(self, days=30):
        """Get customer analytics"""
        from orders.models import Order
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        # Base queryset
        orders = Order.objects.filter(
            created_at__gte=start_date,
            payment_status='paid'
        )
        
        # Filter by shop if specified
        if self.shop:
            orders = orders.filter(items__product__shop=self.shop).distinct()
        elif self.user and self.user.is_trader:
            orders = orders.filter(items__product__shop__owner=self.user).distinct()
        
        # Customer metrics
        total_customers = orders.values('customer').distinct().count()
        new_customers = orders.filter(
            customer__date_joined__gte=start_date
        ).values('customer').distinct().count()
        
        # Top customers
        top_customers = orders.values(
            'customer__username',
            'customer__email'
        ).annotate(
            total_orders=Count('id'),
            total_spent=Sum('total_amount')
        ).order_by('-total_spent')[:10]
        
        return {
            'total_customers': total_customers,
            'new_customers': new_customers,
            'top_customers': list(top_customers)
        }


class InventoryAnalytics:
    """Inventory analytics and alerts"""
    
    def __init__(self, user=None, shop=None):
        self.user = user
        self.shop = shop
    
    def get_low_stock_products(self):
        """Get products with low stock"""
        from shops.models import Product
        
        # Base queryset
        products = Product.objects.filter(is_active=True)
        
        # Filter by shop if specified
        if self.shop:
            products = products.filter(shop=self.shop)
        elif self.user and self.user.is_trader:
            products = products.filter(shop__owner=self.user)
        
        # Filter low stock products
        low_stock = products.filter(
            stock_quantity__lte=F('low_stock_threshold')
        ).values(
            'name',
            'sku',
            'stock_quantity',
            'low_stock_threshold',
            'shop__name'
        )
        
        return list(low_stock)
    
    def get_out_of_stock_products(self):
        """Get out of stock products"""
        from shops.models import Product
        
        # Base queryset
        products = Product.objects.filter(is_active=True, stock_quantity=0)
        
        # Filter by shop if specified
        if self.shop:
            products = products.filter(shop=self.shop)
        elif self.user and self.user.is_trader:
            products = products.filter(shop__owner=self.user)
        
        return products.values(
            'name',
            'sku',
            'shop__name',
            'created_at'
        )
    
    def get_inventory_value(self):
        """Calculate total inventory value"""
        from shops.models import Product
        
        # Base queryset
        products = Product.objects.filter(is_active=True)
        
        # Filter by shop if specified
        if self.shop:
            products = products.filter(shop=self.shop)
        elif self.user and self.user.is_trader:
            products = products.filter(shop__owner=self.user)
        
        # Calculate inventory value
        inventory_value = products.aggregate(
            total_value=Sum(F('stock_quantity') * F('price'))
        )['total_value'] or Decimal('0.00')
        
        total_products = products.count()
        total_quantity = products.aggregate(Sum('stock_quantity'))['stock_quantity__sum'] or 0
        
        return {
            'total_value': float(inventory_value),
            'total_products': total_products,
            'total_quantity': total_quantity
        }


class ReportGenerator:
    """Generate various business reports"""
    
    @staticmethod
    def generate_sales_report(user=None, shop=None, start_date=None, end_date=None):
        """Generate comprehensive sales report"""
        if not start_date:
            start_date = timezone.now() - timedelta(days=30)
        if not end_date:
            end_date = timezone.now()
        
        analytics = SalesAnalytics(user=user, shop=shop)
        
        # Get various metrics
        days = (end_date - start_date).days
        sales_summary = analytics.get_sales_summary(days=days)
        daily_sales = analytics.get_daily_sales(days=days)
        top_products = analytics.get_top_products(days=days)
        category_performance = analytics.get_category_performance(days=days)
        customer_analytics = analytics.get_customer_analytics(days=days)
        
        return {
            'report_type': 'sales_report',
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'days': days
            },
            'sales_summary': sales_summary,
            'daily_sales': daily_sales,
            'top_products': top_products,
            'category_performance': category_performance,
            'customer_analytics': customer_analytics,
            'generated_at': timezone.now().isoformat()
        }
    
    @staticmethod
    def generate_inventory_report(user=None, shop=None):
        """Generate inventory report"""
        inventory = InventoryAnalytics(user=user, shop=shop)
        
        return {
            'report_type': 'inventory_report',
            'inventory_value': inventory.get_inventory_value(),
            'low_stock_products': inventory.get_low_stock_products(),
            'out_of_stock_products': list(inventory.get_out_of_stock_products()),
            'generated_at': timezone.now().isoformat()
        }
