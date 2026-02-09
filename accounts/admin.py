from django.contrib import admin

from .models import UserProfile, Address, Wishlist, Notification, SupportMessage


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    fields = ('full_name', 'phone_number', 'address', 'postal_code', 'city', 'created_at')
    readonly_fields = ('created_at',)


class WishlistInline(admin.TabularInline):
    model = Wishlist
    extra = 0
    fields = ('product', 'added_at')
    readonly_fields = ('added_at',)


class NotificationInline(admin.TabularInline):
    model = Notification
    extra = 0
    fields = ('title', 'message', 'is_read', 'timestamp')
    readonly_fields = ('timestamp',)


class SupportMessageInline(admin.TabularInline):
    model = SupportMessage
    extra = 0
    fields = ('message', 'created_at', 'is_read', 'response', 'responded_at')
    readonly_fields = ('created_at', 'message', 'response', 'responded_at')
    can_delete = False


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_user_display', 'phone_number', 'email', 'first_name', 'last_name', 'gender', 'birth_date')
    list_filter = ('gender', 'birth_date')
    search_fields = ('user__username', 'phone_number', 'email', 'first_name', 'last_name')
    readonly_fields = ('user',)
    fieldsets = (
        ('کاربر', {'fields': ('user',)}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'phone_number', 'email', 'gender', 'birth_date')}),
    )
    inlines = [AddressInline, WishlistInline, NotificationInline, SupportMessageInline]
    
    def get_user_display(self, obj):
        return obj.user.username if obj.user else "نامشخص"
    get_user_display.short_description = 'نام کاربری'


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ('get_user_display', 'created_at', 'is_read', 'responded_at')
    list_filter = ('is_read', 'created_at', 'responded_at')
    search_fields = ('user__user__username', 'user__user__email', 'message')
    readonly_fields = ('created_at', 'message', 'user')
    fieldsets = (
        ('کاربر و پیام', {'fields': ('user', 'message', 'created_at')}),
        ('پاسخ', {'fields': ('is_read', 'response', 'responded_at')}),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'user__user')
    
    def get_user_display(self, obj):
        if obj.user.first_name or obj.user.last_name:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return obj.user.user.username if obj.user.user else "نامشخص"
    get_user_display.short_description = 'کاربر'


# Register your models here.
