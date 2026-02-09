# nafis/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import (SlideShow, Category, Size, Material, Apparel, ApparelImage, 
                     Gender, KidsGender, ProductType, Style, Color, 
                     Contact, Discount, Inventory, Order, OrderItem, CartItem, Announcement)


@admin.register(SlideShow)
class SlideShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)

# ثبت مدل جدید اطلاعیه‌ها
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(KidsGender)
class KidsGenderAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code', 'color_preview')
    search_fields = ('name',)
    
    def color_preview(self, obj):
        if obj.hex_code:
            return format_html(
                f'<div style="width: 30px; height: 20px; background-color: {obj.hex_code}; border: 1px solid #ccc;"></div>'
            )
        return "-"
    color_preview.short_description = "پیش‌نمایش رنگ"


class ApparelImageInline(admin.TabularInline):
    model = ApparelImage
    extra = 1
    verbose_name = "تصویر اضافی"
    verbose_name_plural = "تصاویر اضافی"


@admin.register(Apparel)
class ApparelAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'gender', 'product_type', 'price', 'has_discount', 'total_inventory', 'main_image_preview', 'created_at')
    search_fields = ('name', 'code', 'description')
    list_filter = ('gender', 'product_type', 'material', 'created_at')
    inlines = [ApparelImageInline]
    readonly_fields = ('code',) # کد محصول خودکار است و نباید ویرایش شود
    filter_horizontal = ('style', 'color',) # برای انتخاب راحت‌تر
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'code', 'price', 'description', 'main_image')
        }),
        ('دسته‌بندی و جزئیات', {
            'fields': ('category', 'gender', 'kids_gender', 'product_type', 'material', 'style', 'color')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('inventory')

    def has_discount(self, obj):
        return obj.has_discount()
    has_discount.boolean = True
    has_discount.short_description = 'تخفیف فعال'

    def total_inventory(self, obj):
        total = sum(inv.quantity for inv in obj.inventory.all())
        if total == 0:
            return format_html('<span style="color: red;">ناموجود</span>')
        return total
    total_inventory.short_description = 'موجودی کل'

    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html(f'<img src="{obj.main_image.url}" style="width: 50px; height: auto;" />')
        return "بدون تصویر"
    main_image_preview.short_description = "تصویر اصلی"


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('get_apparel_name', 'get_apparel_code', 'size', 'color', 'quantity', 'inventory_status', 'updated_at')
    search_fields = ('apparel__name', 'apparel__code', 'size__name', 'color__name')
    list_filter = ('apparel__gender', 'size', 'color', 'updated_at')
    list_editable = ('quantity',) # امکان ویرایش مستقیم موجودی از لیست
    autocomplete_fields = ('apparel',)
    list_per_page = 25

    def get_apparel_name(self, obj):
        return obj.apparel.name
    get_apparel_name.short_description = 'نام محصول'
    get_apparel_name.admin_order_field = 'apparel__name'

    def get_apparel_code(self, obj):
        return obj.apparel.code
    get_apparel_code.short_description = 'کد محصول'
    get_apparel_code.admin_order_field = 'apparel__code'
    
    def inventory_status(self, obj):
        if obj.quantity == 0:
            return format_html('<span style="color: red; font-weight: bold;">ناموجود</span>')
        elif obj.quantity < 5:
            return format_html('<span style="color: orange;">کم</span>')
        else:
            return format_html('<span style="color: green;">موجود</span>')
    inventory_status.short_description = 'وضعیت انبار'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('apparel', 'discount_percentage', 'start_date', 'end_date', 'is_active')
    search_fields = ('apparel__name',)
    list_filter = ('start_date', 'end_date')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    search_fields = ('user__username', 'id')
    list_filter = ('status', 'created_at')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'apparel', 'size', 'color', 'quantity', 'price')
    search_fields = ('apparel__name', 'order__id')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'apparel', 'size', 'color', 'quantity', 'created_at')
    search_fields = ('user__username', 'apparel__name')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')


admin.site.site_header = 'پنل مدیریت فروشگاه نفیس'
admin.site.site_title = 'پنل مدیریت'
admin.site.index_title = 'خوش آمدید به پنل مدیریت'