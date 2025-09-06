from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    # Admin dashboard
    path('', views.dashboard, name='dashboard'),
    path('users/', views.user_management, name='user_management'),
    path('traders/', views.trader_management, name='trader_management'),
    path('traders/<int:trader_id>/approve/', views.approve_trader, name='approve_trader'),
    path('traders/<int:trader_id>/reject/', views.reject_trader, name='reject_trader'),
    path('traders/<int:trader_id>/suspend/', views.suspend_trader, name='suspend_trader'),
    path('traders/<int:trader_id>/details/', views.trader_details, name='trader_details'),
    path('shops/', views.shop_management, name='shop_management'),
    path('shops/<int:shop_id>/approve/', views.approve_shop, name='approve_shop'),
    path('shops/<int:shop_id>/reject/', views.reject_shop, name='reject_shop'),
    path('shops/<int:shop_id>/details/', views.shop_details, name='shop_details'),
    path('orders/', views.order_management, name='order_management'),
    path('reports/', views.reports, name='reports'),
]
