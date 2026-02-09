# nafis/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import (Apparel, SlideShow, Category, ApparelImage, Gender, 
                     ProductType, Style, Color, Size, Inventory, CartItem, 
                     Order, OrderItem, Announcement)
from .forms import ContactForm


def index(request):
    slideshows = SlideShow.objects.order_by('-created_at')[:4]
    announcements = Announcement.objects.order_by('-created_at')[:4]
    
    # تغییر: نمایش 12 محصول جدید (به جای 8، برای اسلایدر با بقیه متحرک)
    newest_apparels = Apparel.objects.order_by('-created_at')[:18]
    
    # تغییر: نمایش 12 محصول تخفیف خورده
    discounted_apparels = Apparel.objects.filter(
        discounts__start_date__lte=timezone.now(), 
        discounts__end_date__gte=timezone.now()
    ).distinct().order_by('-created_at')[:18]

    men_gender = Gender.objects.filter(name='مردانه').first()
    women_gender = Gender.objects.filter(name='زنانه').first()
    kids_gender = Gender.objects.filter(name='بچگانه').first()

    # تغییر: نمایش 12 محصول مردانه
    men_apparels = Apparel.objects.filter(gender=men_gender).order_by('-created_at')[:18] if men_gender else Apparel.objects.none()
    
    # تغییر: نمایش 12 محصول زنانه
    women_apparels = Apparel.objects.filter(gender=women_gender).order_by('-created_at')[:18] if women_gender else Apparel.objects.none()
    
    # تغییر: نمایش 12 محصول بچگانه
    kids_apparels = Apparel.objects.filter(gender=kids_gender).order_by('-created_at')[:18] if kids_gender else Apparel.objects.none()
    
    context = {
        'slideshows': slideshows,
        'announcements': announcements,
        'newest_apparels': newest_apparels,
        'discounted_apparels': discounted_apparels,
        'men_apparels': men_apparels,
        'women_apparels': women_apparels,
        'kids_apparels': kids_apparels,
    }
    return render(request, "nafis/index.html", context)


def apparel_detail(request, slug):
    apparel = get_object_or_404(Apparel.objects.prefetch_related('style', 'color', 'images'), slug=slug)
    
    related_apparels = Apparel.objects.none()
    if apparel.product_type:
        related_apparels = Apparel.objects.filter(
            product_type=apparel.product_type,
            gender=apparel.gender
        ).exclude(slug=apparel.slug).select_related('gender')[:4]
    
    inventory_info = Inventory.objects.filter(apparel=apparel, quantity__gt=0)
    available_sizes = Size.objects.filter(inventory__in=inventory_info).distinct()
    available_colors = Color.objects.filter(inventory__in=inventory_info).distinct()
    
    context = {
        'apparel': apparel,
        'related_apparels': related_apparels,
        'available_sizes': available_sizes,
        'available_colors': available_colors,
    }
    return render(request, "nafis/apparel_detail.html", context)


def search_page(request):
    query = request.GET.get('q')
    apparels = Apparel.objects.none()

    if query:
        apparels = Apparel.objects.filter(
            Q(name__icontains=query) | Q(code__icontains=query) |
            Q(category__name__icontains=query) | Q(product_type__name__icontains=query) |
            Q(description__icontains=query)
        ).distinct()

    return render(request, "nafis/search_page.html", {'apparels': apparels, 'query': query})

# این تابع دوباره اضافه شد
def products(request):
    men_gender = Gender.objects.filter(name='مردانه').first()
    women_gender = Gender.objects.filter(name='زنانه').first()
    kids_gender = Gender.objects.filter(name='بچگانه').first()

    men_apparels = Apparel.objects.filter(gender=men_gender).order_by('-created_at')[:12] if men_gender else Apparel.objects.none()
    women_apparels = Apparel.objects.filter(gender=women_gender).order_by('-created_at')[:12] if women_gender else Apparel.objects.none()
    kids_apparels = Apparel.objects.filter(gender=kids_gender).order_by('-created_at')[:12] if kids_gender else Apparel.objects.none()

    context = {
        'men_apparels': men_apparels,
        'women_apparels': women_apparels,
        'kids_apparels': kids_apparels
    }
    return render(request, "nafis/products.html", context)


def men_products(request):
    men_gender = get_object_or_404(Gender, name='مردانه')
    apparels = Apparel.objects.filter(gender=men_gender).order_by('-created_at')
    
    context = {'apparels': apparels, 'category_name': 'محصولات مردانه'}
    return render(request, "nafis/category_products.html", context)


def women_products(request):
    women_gender = get_object_or_404(Gender, name='زنانه')
    apparels = Apparel.objects.filter(gender=women_gender).order_by('-created_at')
    
    context = {'apparels': apparels, 'category_name': 'محصولات زنانه'}
    return render(request, "nafis/category_products.html", context)


def kids_products(request):
    kids_gender = get_object_or_404(Gender, name='بچگانه')
    apparels = Apparel.objects.filter(gender=kids_gender).order_by('-created_at')
    
    context = {'apparels': apparels, 'category_name': 'محصولات بچگانه'}
    return render(request, "nafis/category_products.html", context)


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'پیام شما با موفقیت دریافت شد!')
            return redirect('nafis:contact')
        else:
            messages.error(request, 'خطا در ارسال پیام. لطفا دوباره تلاش کنید.')
    else:
        form = ContactForm()
    return render(request, 'nafis/contact.html', {'form': form})


@login_required(login_url='accounts:login') # فرض بر این است که اپ accounts و URL الگو login وجود دارد
def add_to_cart(request, apparel_id):
    apparel = get_object_or_404(Apparel, id=apparel_id)
    if request.method == 'POST':
        size_id = request.POST.get('size')
        color_id = request.POST.get('color')
        quantity = int(request.POST.get('quantity', 1))
        
        if not all([size_id, color_id]):
            messages.error(request, 'لطفا سایز و رنگ را انتخاب کنید.')
            return redirect('nafis:apparel_detail', slug=apparel.slug)
        
        size = get_object_or_404(Size, id=size_id)
        color = get_object_or_404(Color, id=color_id)
        
        try:
            inventory = Inventory.objects.get(apparel=apparel, size=size, color=color)
            if inventory.quantity >= quantity:
                cart_item, created = CartItem.objects.get_or_create(
                    user=request.user, apparel=apparel, size=size, color=color,
                    defaults={'quantity': quantity}
                )
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
                
                messages.success(request, f'{quantity} عدد از محصول {apparel.name} به سبد خرید اضافه شد.')
                return redirect('nafis:shopping_cart')
            else:
                messages.error(request, 'موجودی انبار کافی نیست.')
        except Inventory.DoesNotExist:
            messages.error(request, 'این محصول با مشخصات انتخابی موجود نیست.')
    
    return redirect('nafis:apparel_detail', slug=apparel.slug)


@login_required(login_url='accounts:login')
def shopping_cart(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('apparel', 'size', 'color')
    total_price = sum(item.quantity * item.apparel.get_discounted_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'nafis/shopping_cart.html', context)


@login_required(login_url='accounts:login')
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'محصول از سبد خرید حذف شد.')
    return redirect('nafis:shopping_cart')


@login_required(login_url='accounts:login')
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.warning(request, 'سبد خرید شما خالی است.')
        return redirect('nafis:index')

    total_price = sum(item.quantity * item.apparel.get_discounted_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'nafis/checkout.html', context)


@login_required(login_url='accounts:login')
def place_order(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items:
            messages.error(request, 'سبد خرید شما برای ثبت سفارش خالی است.')
            return redirect('nafis:shopping_cart')
        
        total_price = sum(item.quantity * item.apparel.get_discounted_price() for item in cart_items)
        order = Order.objects.create(user=request.user, total_price=total_price)
        
        order_items_to_create = []
        for item in cart_items:
            inventory = Inventory.objects.get(apparel=item.apparel, size=item.size, color=item.color)
            if inventory.quantity < item.quantity:
                messages.error(request, f"موجودی محصول {item.apparel.name} کافی نیست.")
                order.delete() # سفارش ناموفق را حذف کن
                return redirect('nafis:shopping_cart')

            inventory.quantity -= item.quantity
            inventory.save()
            
            order_items_to_create.append(
                OrderItem(
                    order=order, apparel=item.apparel, size=item.size,
                    color=item.color, quantity=item.quantity,
                    price=item.apparel.get_discounted_price()
                )
            )

        OrderItem.objects.bulk_create(order_items_to_create)
        cart_items.delete()
        
        messages.success(request, f'سفارش شما با شماره {order.id} با موفقیت ثبت شد.')
        return redirect('nafis:index')

    return redirect('nafis:checkout')