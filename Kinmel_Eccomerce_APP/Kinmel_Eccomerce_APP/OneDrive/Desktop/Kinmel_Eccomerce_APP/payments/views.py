from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order


@login_required
def process_payment(request, order_id):
    """Process payment for order"""
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    if order.payment_status == 'paid':
        messages.info(request, 'This order has already been paid.')
        return redirect('orders:order_detail', order_id=order.id)

    context = {
        'order': order,
    }
    return render(request, 'payments/process_payment.html', context)


@login_required
def payment_success(request, order_id):
    """Payment success page"""
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    # Update order status
    order.payment_status = 'paid'
    order.status = 'confirmed'
    order.save()

    context = {
        'order': order,
    }
    return render(request, 'payments/payment_success.html', context)


@login_required
def payment_cancel(request, order_id):
    """Payment cancelled page"""
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    context = {
        'order': order,
    }
    return render(request, 'payments/payment_cancel.html', context)


@csrf_exempt
def paypal_webhook(request):
    """Handle PayPal webhooks"""
    # This will be implemented when we integrate PayPal
    return HttpResponse(status=200)
