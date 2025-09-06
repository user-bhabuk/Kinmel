from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from users.models import User
from shops.models import Shop, Product, Category
from orders.models import Order
from utils.email_service import EmailNotificationService
# from utils.analytics import SalesAnalytics, ReportGenerator  # Will be imported when needed


@login_required
def dashboard(request):
    """Admin dashboard with comprehensive analytics"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('shops:home')

    # Time periods for analytics
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)
    last_7_days = today - timedelta(days=7)

    # Basic stats
    total_users = User.objects.count()
    total_traders = User.objects.filter(role='trader').count()
    total_customers = User.objects.filter(role='customer').count()
    total_shops = Shop.objects.count()
    total_products = Product.objects.count()
    total_categories = Category.objects.count()

    # Order stats
    total_orders = Order.objects.count()
    orders_last_30_days = Order.objects.filter(created_at__gte=last_30_days).count()
    orders_last_7_days = Order.objects.filter(created_at__gte=last_7_days).count()

    # Revenue stats
    total_revenue = Order.objects.filter(payment_status='paid').aggregate(
        Sum('total_amount'))['total_amount__sum'] or 0
    revenue_last_30_days = Order.objects.filter(
        payment_status='paid',
        created_at__gte=last_30_days
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # Pending approvals
    pending_traders = User.objects.filter(role='trader', is_approved=False).count()
    pending_shops = Shop.objects.filter(is_approved=False).count()

    # Recent activity
    recent_orders = Order.objects.select_related('customer').order_by('-created_at')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_shops = Shop.objects.select_related('owner').order_by('-created_at')[:5]

    # Analytics data (simplified for now)
    sales_summary = {'total_revenue': float(total_revenue), 'total_orders': total_orders}
    daily_sales = []  # Will be populated with actual data
    top_products = []  # Will be populated with actual data
    category_performance = []  # Will be populated with actual data

    context = {
        # Basic stats
        'total_users': total_users,
        'total_traders': total_traders,
        'total_customers': total_customers,
        'total_shops': total_shops,
        'total_products': total_products,
        'total_categories': total_categories,
        'total_orders': total_orders,
        'orders_last_30_days': orders_last_30_days,
        'orders_last_7_days': orders_last_7_days,
        'total_revenue': total_revenue,
        'revenue_last_30_days': revenue_last_30_days,

        # Pending approvals
        'pending_traders': pending_traders,
        'pending_shops': pending_shops,

        # Recent activity
        'recent_orders': recent_orders,
        'recent_users': recent_users,
        'recent_shops': recent_shops,

        # Analytics
        'sales_summary': sales_summary,
        'daily_sales': daily_sales,
        'top_products': top_products,
        'category_performance': category_performance,
    }
    return render(request, 'adminpanel/dashboard.html', context)


@login_required
def user_management(request):
    """User management"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('shops:home')

    users = User.objects.all().order_by('-date_joined')
    return render(request, 'adminpanel/user_management.html', {'users': users})


@login_required
def trader_management(request):
    """Trader management"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('shops:home')

    traders = User.objects.filter(role='trader').order_by('-date_joined')
    return render(request, 'adminpanel/trader_management.html', {'traders': traders})


@login_required
@require_POST
def approve_trader(request, trader_id):
    """Approve trader"""
    if not request.user.is_admin:
        return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)

    try:
        trader = User.objects.get(id=trader_id, role='trader')
        trader.is_active = True
        trader.is_approved = True  # This is the key field for trader approval
        trader.save()

        # Send approval email notification
        email_sent = EmailNotificationService.send_trader_approval_email(trader)

        success_message = f'Trader {trader.username} approved successfully'
        if email_sent:
            success_message += ' and notification email sent'
        else:
            success_message += ' (email notification failed)'

        return JsonResponse({'success': True, 'message': success_message})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Trader not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@login_required
@require_POST
def reject_trader(request, trader_id):
    """Reject trader"""
    if not request.user.is_admin:
        return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)

    try:
        trader = User.objects.get(id=trader_id, role='trader')

        # Send rejection email before deleting
        EmailNotificationService.send_trader_rejection_email(trader, "Application did not meet our requirements")

        trader.delete()  # Or set is_active=False and add rejection reason

        return JsonResponse({'success': True, 'message': f'Trader application rejected and notification sent'})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Trader not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@login_required
@require_POST
def suspend_trader(request, trader_id):
    """Suspend trader"""
    if not request.user.is_admin:
        return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)

    try:
        trader = User.objects.get(id=trader_id, role='trader')
        trader.is_active = False
        trader.save()

        return JsonResponse({'success': True, 'message': f'Trader {trader.username} suspended'})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Trader not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@login_required
def trader_details(request, trader_id):
    """Get trader details"""
    if not request.user.is_admin:
        return JsonResponse({'error': 'Access denied'}, status=403)

    try:
        trader = User.objects.get(id=trader_id, role='trader')

        # Get trader's shops
        shops = trader.shops.all() if hasattr(trader, 'shops') else []

        context = {
            'trader': trader,
            'shops': shops,
        }

        return render(request, 'adminpanel/trader_details_modal.html', context)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Trader not found'}, status=404)


@login_required
def shop_management(request):
    """Shop management"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('shops:home')

    shops = Shop.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/shop_management.html', {'shops': shops})


@login_required
@require_POST
def approve_shop(request, shop_id):
    """Approve shop"""
    if not request.user.is_admin:
        return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)

    try:
        shop = Shop.objects.get(id=shop_id)
        shop.is_approved = True
        shop.is_active = True
        shop.save()

        # Send shop approval email notification
        email_sent = EmailNotificationService.send_shop_approval_email(shop)

        success_message = f'Shop {shop.name} approved successfully'
        if email_sent:
            success_message += ' and notification email sent'
        else:
            success_message += ' (email notification failed)'

        return JsonResponse({'success': True, 'message': success_message})
    except Shop.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Shop not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@login_required
@require_POST
def reject_shop(request, shop_id):
    """Reject shop"""
    if not request.user.is_admin:
        return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)

    try:
        shop = Shop.objects.get(id=shop_id)
        shop.is_approved = False
        shop.is_active = False
        shop.save()

        # Send shop rejection email notification
        EmailNotificationService.send_shop_rejection_email(shop, "Shop did not meet our quality standards")

        return JsonResponse({'success': True, 'message': f'Shop {shop.name} rejected and notification sent'})
    except Shop.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Shop not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@login_required
def shop_details(request, shop_id):
    """Get shop details"""
    if not request.user.is_admin:
        return JsonResponse({'error': 'Access denied'}, status=403)

    try:
        shop = Shop.objects.get(id=shop_id)
        products = shop.products.all()[:10]  # Get first 10 products

        context = {
            'shop': shop,
            'products': products,
        }

        return render(request, 'adminpanel/shop_details_modal.html', context)
    except Shop.DoesNotExist:
        return JsonResponse({'error': 'Shop not found'}, status=404)


@login_required
def order_management(request):
    """Order management"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('shops:home')

    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/order_management.html', {'orders': orders})


@login_required
def reports(request):
    """Reports and analytics"""
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('shops:home')

    return render(request, 'adminpanel/reports.html')
