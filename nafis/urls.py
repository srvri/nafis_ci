# nafis/urls.py

from django.urls import path
from . import views

app_name = 'nafis'

urlpatterns = [
    path("", views.index, name="index"),
    path('apparel/<slug:slug>/', views.apparel_detail, name='apparel_detail'),
    path("search/", views.search_page, name="search_page"),
    path('contact/', views.contact_view, name='contact'),
    
    # این سه خط آدرس‌های دسته‌بندی‌های اصلی هستند
    path('men-products/', views.men_products, name='men_products'),
    path('women-products/', views.women_products, name='women_products'),
    path('kids-products/', views.kids_products, name='kids_products'),
    
    # این خط که باعث خطا شده بود، دوباره اضافه شد
    path('products/', views.products, name='products'),
    
    # آدرس‌های مربوط به سبد خرید و سفارش
    path('add-to-cart/<int:apparel_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.shopping_cart, name='shopping_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
]