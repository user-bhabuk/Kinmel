from django.urls import path
from . import views

app_name = 'shops'

urlpatterns = [
    # Public views
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('shop/<int:pk>/', views.shop_detail, name='shop_detail'),
    path('category/<int:pk>/', views.category_products, name='category_products'),
    
    # Trader dashboard
    path('trader/dashboard/', views.trader_dashboard, name='trader_dashboard'),
    path('trader/shop/create/', views.create_shop, name='create_shop'),
    path('trader/shop/<int:pk>/edit/', views.edit_shop, name='edit_shop'),
    path('trader/shop/<int:pk>/products/', views.shop_products, name='shop_products'),
    
    # Product management
    path('trader/shop/<int:shop_pk>/product/create/', views.create_product, name='create_product'),
    path('trader/product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('trader/product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    
    # Reviews
    path('product/<int:product_pk>/review/', views.add_review, name='add_review'),
    
    # Discount requests
    path('trader/discount-requests/', views.discount_requests, name='discount_requests'),
    path('trader/discount-request/create/', views.create_discount_request, name='create_discount_request'),
    
    # AJAX endpoints
    path('api/product/<int:pk>/', views.get_product_info, name='get_product_info'),
]
