from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Shop, Product, Category, ProductImage, DiscountRequest
from .forms import (
    ShopForm, ProductForm, ProductImageFormSet,
    DiscountRequestForm, ProductSearchForm
)


def home(request):
    """Home page with featured products and categories"""
    featured_products = Product.objects.filter(
        is_active=True, is_featured=True, shop__is_active=True, shop__is_approved=True
    )[:8]

    categories = Category.objects.filter(is_active=True)[:6]

    # Latest products
    latest_products = Product.objects.filter(
        is_active=True, shop__is_active=True, shop__is_approved=True
    ).order_by('-created_at')[:8]

    context = {
        'featured_products': featured_products,
        'categories': categories,
        'latest_products': latest_products,
    }
    return render(request, 'shops/home.html', context)


def product_list(request):
    """Product listing with search and filters"""
    form = ProductSearchForm(request.GET)
    products = Product.objects.filter(
        is_active=True, shop__is_active=True, shop__is_approved=True
    )

    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        condition = form.cleaned_data.get('condition')
        in_stock_only = form.cleaned_data.get('in_stock_only')

        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(brand__icontains=query)
            )

        if category:
            products = products.filter(category=category)

        if min_price:
            products = products.filter(price__gte=min_price)

        if max_price:
            products = products.filter(price__lte=max_price)

        if condition:
            products = products.filter(condition=condition)

        if in_stock_only:
            products = products.filter(stock_quantity__gt=0)

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
        'products': page_obj,
    }
    return render(request, 'shops/product_list.html', context)


def product_detail(request, pk):
    """Product detail page"""
    product = get_object_or_404(
        Product,
        pk=pk,
        is_active=True,
        shop__is_active=True,
        shop__is_approved=True
    )

    # Get product images
    images = product.images.all()

    # Reviews will be implemented later
    reviews = []
    can_review = False

    # Related products
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True,
        shop__is_active=True,
        shop__is_approved=True
    ).exclude(pk=product.pk)[:4]

    context = {
        'product': product,
        'images': images,
        'reviews': reviews,
        'can_review': can_review,
        'related_products': related_products,
    }
    return render(request, 'shops/product_detail.html', context)


def shop_detail(request, pk):
    """Shop detail page"""
    shop = get_object_or_404(Shop, pk=pk, is_active=True, is_approved=True)

    # Get shop products
    products = shop.products.filter(is_active=True)

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'shop': shop,
        'page_obj': page_obj,
        'products': page_obj,
    }
    return render(request, 'shops/shop_detail.html', context)


def category_products(request, pk):
    """Products by category"""
    category = get_object_or_404(Category, pk=pk, is_active=True)

    products = Product.objects.filter(
        category=category,
        is_active=True,
        shop__is_active=True,
        shop__is_approved=True
    )

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
        'products': page_obj,
    }
    return render(request, 'shops/category_products.html', context)


# Trader Dashboard Views
@login_required
def trader_dashboard(request):
    """Trader dashboard"""
    if not request.user.is_trader:
        messages.error(request, 'Access denied. Trader account required.')
        return redirect('shops:home')

    if not request.user.is_approved:
        messages.warning(request, 'Your trader account is pending approval.')
        return render(request, 'shops/trader_pending.html')

    # Get trader's shops and products
    shops = request.user.shops.all()
    total_products = Product.objects.filter(shop__owner=request.user).count()
    active_products = Product.objects.filter(shop__owner=request.user, is_active=True).count()

    # Recent orders (will be implemented in orders app)
    # recent_orders = OrderItem.objects.filter(product__shop__owner=request.user)[:5]

    context = {
        'shops': shops,
        'total_products': total_products,
        'active_products': active_products,
        # 'recent_orders': recent_orders,
    }
    return render(request, 'shops/trader_dashboard.html', context)


@login_required
def create_shop(request):
    """Create a new shop"""
    if not request.user.is_trader or not request.user.is_approved:
        messages.error(request, 'Access denied.')
        return redirect('shops:home')

    # Check if trader can create more shops
    if request.user.shops.count() >= 4:
        messages.error(request, 'You can only create up to 4 shops.')
        return redirect('shops:trader_dashboard')

    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            shop.save()
            messages.success(request, 'Shop created successfully! Waiting for admin approval.')
            return redirect('shops:trader_dashboard')
    else:
        form = ShopForm()

    return render(request, 'shops/create_shop.html', {'form': form})


@login_required
def edit_shop(request, pk):
    """Edit shop"""
    shop = get_object_or_404(Shop, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Shop updated successfully!')
            return redirect('shops:trader_dashboard')
    else:
        form = ShopForm(instance=shop)

    return render(request, 'shops/edit_shop.html', {'form': form, 'shop': shop})


@login_required
def shop_products(request, pk):
    """List products for a specific shop"""
    shop = get_object_or_404(Shop, pk=pk, owner=request.user)
    products = shop.products.all()

    # Pagination
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'shop': shop,
        'page_obj': page_obj,
        'products': page_obj,
    }
    return render(request, 'shops/shop_products.html', context)


@login_required
def create_product(request, shop_pk):
    """Create a new product"""
    shop = get_object_or_404(Shop, pk=shop_pk, owner=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        formset = ProductImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.shop = shop
            product.save()

            formset.instance = product
            formset.save()

            messages.success(request, 'Product created successfully!')
            return redirect('shops:shop_products', pk=shop.pk)
    else:
        form = ProductForm()
        formset = ProductImageFormSet()

    context = {
        'form': form,
        'formset': formset,
        'shop': shop,
    }
    return render(request, 'shops/create_product.html', context)


@login_required
def edit_product(request, pk):
    """Edit product"""
    product = get_object_or_404(Product, pk=pk, shop__owner=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('shops:shop_products', pk=product.shop.pk)
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)

    context = {
        'form': form,
        'formset': formset,
        'product': product,
    }
    return render(request, 'shops/edit_product.html', context)


@login_required
@require_POST
def delete_product(request, pk):
    """Delete product"""
    product = get_object_or_404(Product, pk=pk, shop__owner=request.user)
    shop_pk = product.shop.pk
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('shops:shop_products', pk=shop_pk)


# Review functionality will be implemented later
def add_review(request, product_pk):
    """Add product review - Coming soon"""
    messages.info(request, 'Review functionality coming soon!')
    return redirect('shops:product_detail', pk=product_pk)


# Discount Request Views
@login_required
def discount_requests(request):
    """List trader's discount requests"""
    if not request.user.is_trader:
        messages.error(request, 'Access denied.')
        return redirect('shops:home')

    requests = DiscountRequest.objects.filter(trader=request.user).order_by('-created_at')

    # Pagination
    paginator = Paginator(requests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'requests': page_obj,
    }
    return render(request, 'shops/discount_requests.html', context)


@login_required
def create_discount_request(request):
    """Create discount request"""
    if not request.user.is_trader:
        messages.error(request, 'Access denied.')
        return redirect('shops:home')

    if request.method == 'POST':
        form = DiscountRequestForm(request.POST, user=request.user)
        if form.is_valid():
            discount_request = form.save(commit=False)
            discount_request.trader = request.user
            discount_request.save()
            messages.success(request, 'Discount request submitted successfully!')
            return redirect('shops:discount_requests')
    else:
        form = DiscountRequestForm(user=request.user)

    return render(request, 'shops/create_discount_request.html', {'form': form})


# AJAX Views
def get_product_info(request, pk):
    """Get product info for AJAX requests"""
    try:
        product = Product.objects.get(pk=pk, is_active=True)
        data = {
            'name': product.name,
            'price': str(product.price),
            'stock': product.stock_quantity,
            'in_stock': product.is_in_stock,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
