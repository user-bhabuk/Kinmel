from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem, Invoice
from shops.models import Product


@login_required
def cart_view(request):
    """View shopping cart"""
    if not request.user.is_customer:
        messages.error(request, 'Only customers can access the shopping cart.')
        return redirect('shops:home')

    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_items = cart.items.all().select_related('product', 'product__shop')

    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'orders/cart.html', context)


@login_required
@require_POST
def add_to_cart(request, product_id):
    """Add product to cart"""
    if not request.user.is_customer:
        return JsonResponse({'error': 'Only customers can add items to cart'}, status=403)

    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))

    if quantity <= 0:
        return JsonResponse({'error': 'Invalid quantity'}, status=400)

    if quantity > product.stock_quantity:
        return JsonResponse({'error': f'Only {product.stock_quantity} items available'}, status=400)

    cart, created = Cart.objects.get_or_create(customer=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        # Update quantity if item already exists
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock_quantity:
            return JsonResponse({'error': f'Only {product.stock_quantity} items available'}, status=400)
        cart_item.quantity = new_quantity
        cart_item.save()

    return JsonResponse({
        'success': True,
        'message': f'{product.name} added to cart',
        'cart_count': cart.total_items
    })


@login_required
@require_POST
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    if not request.user.is_customer:
        return JsonResponse({'error': 'Access denied'}, status=403)

    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer=request.user)
    quantity = int(request.POST.get('quantity', 1))

    if quantity <= 0:
        cart_item.delete()
        return JsonResponse({'success': True, 'message': 'Item removed from cart'})

    if quantity > cart_item.product.stock_quantity:
        return JsonResponse({'error': f'Only {cart_item.product.stock_quantity} items available'}, status=400)

    cart_item.quantity = quantity
    cart_item.save()

    return JsonResponse({
        'success': True,
        'message': 'Cart updated',
        'item_total': float(cart_item.total_price),
        'cart_total': float(cart_item.cart.total_amount)
    })


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    if not request.user.is_customer:
        return JsonResponse({'error': 'Access denied'}, status=403)

    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer=request.user)
    cart_item.delete()

    return JsonResponse({'success': True, 'message': 'Item removed from cart'})


@login_required
def checkout(request):
    """Checkout process"""
    if not request.user.is_customer:
        messages.error(request, 'Only customers can checkout.')
        return redirect('shops:home')

    cart = get_object_or_404(Cart, customer=request.user)

    if not cart.items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('orders:cart')

    # Check stock availability
    for item in cart.items.all():
        if item.quantity > item.product.stock_quantity:
            messages.error(request, f'Only {item.product.stock_quantity} units of {item.product.name} available.')
            return redirect('orders:cart')

    if request.method == 'POST':
        # Process checkout
        with transaction.atomic():
            # Create order
            order = Order.objects.create(
                customer=request.user,
                shipping_name=request.POST.get('shipping_name'),
                shipping_email=request.POST.get('shipping_email'),
                shipping_phone=request.POST.get('shipping_phone'),
                shipping_address=request.POST.get('shipping_address'),
                shipping_city=request.POST.get('shipping_city'),
                shipping_state=request.POST.get('shipping_state'),
                shipping_postal_code=request.POST.get('shipping_postal_code'),
                customer_notes=request.POST.get('customer_notes', ''),
            )

            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

                # Reduce product stock
                cart_item.product.reduce_stock(cart_item.quantity)

            # Calculate order totals
            order.calculate_totals()

            # Clear cart
            cart.clear()

            # Create invoice
            Invoice.objects.create(order=order)

            messages.success(request, f'Order {order.order_number} placed successfully!')
            return redirect('payments:process_payment', order_id=order.id)

    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_history(request):
    """Customer order history"""
    if not request.user.is_customer:
        messages.error(request, 'Only customers can view order history.')
        return redirect('shops:home')

    orders = Order.objects.filter(customer=request.user).order_by('-created_at')

    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'orders': page_obj,
    }
    return render(request, 'orders/order_history.html', context)


@login_required
def order_detail(request, order_id):
    """Order detail view"""
    order = get_object_or_404(Order, id=order_id)

    # Check permissions
    if request.user.is_customer and order.customer != request.user:
        messages.error(request, 'You can only view your own orders.')
        return redirect('orders:order_history')
    elif request.user.is_trader:
        # Trader can only view orders containing their products
        if not order.items.filter(product__shop__owner=request.user).exists():
            messages.error(request, 'You can only view orders containing your products.')
            return redirect('shops:trader_dashboard')
    elif not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('shops:home')

    order_items = order.items.all().select_related('product', 'product__shop')

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required
@require_POST
def cancel_order(request, order_id):
    """Cancel order"""
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    if not order.can_cancel:
        messages.error(request, 'This order cannot be cancelled.')
        return redirect('orders:order_detail', order_id=order.id)

    # Restore product stock
    for item in order.items.all():
        item.product.stock_quantity += item.quantity
        item.product.save()

    order.status = 'cancelled'
    order.save()

    messages.success(request, f'Order {order.order_number} has been cancelled.')
    return redirect('orders:order_detail', order_id=order.id)


# Wishlist functionality will be implemented later
def wishlist_view(request):
    """View wishlist - Coming soon"""
    messages.info(request, 'Wishlist functionality coming soon!')
    return redirect('shops:home')

def add_to_wishlist(request, product_id):
    """Add product to wishlist - Coming soon"""
    return JsonResponse({'success': False, 'message': 'Wishlist functionality coming soon!'})

def remove_from_wishlist(request, item_id):
    """Remove item from wishlist - Coming soon"""
    return JsonResponse({'success': False, 'message': 'Wishlist functionality coming soon!'})


# AJAX Views
@login_required
def get_cart_count(request):
    """Get cart item count"""
    if not request.user.is_customer:
        return JsonResponse({'count': 0})

    try:
        cart = Cart.objects.get(customer=request.user)
        return JsonResponse({'count': cart.total_items})
    except Cart.DoesNotExist:
        return JsonResponse({'count': 0})
