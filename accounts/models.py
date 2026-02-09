from django.db import models
from django.contrib.auth.models import User
from nafis.models import Apparel

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    phone_number = models.CharField(max_length=11, unique=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='نام خانوادگی')
    email = models.EmailField(blank=True, verbose_name='ایمیل')
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    gender = models.CharField(max_length=10, choices=[('male', 'مرد'), ('female', 'زن'), ('other', 'سایر')], blank=True, verbose_name='جنسیت')

    def __str__(self):
        return f"Profile of {self.user.email}"

class Address(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.city}"


class Wishlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Apparel, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = "علاقه‌مندی"
        verbose_name_plural = "علاقه‌مندی‌ها"

    def __str__(self):
        return f"{self.product.name} در علاقه‌مندی‌های {self.user.user.username}"


class Notification(models.Model):
    """Simple Notification model for user messages/alerts.

    Fields:
    - user: recipient user
    - title: short title
    - message: longer message/body
    - link: optional URL or path related to notification (can be blank)
    - is_read: whether the user has read the notification
    - timestamp: creation time
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    link = models.CharField(max_length=500, blank=True, help_text='Optional URL/path for the notification')
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "اعلان"
        verbose_name_plural = "اعلان‌ها"

    def __str__(self):
        return f"Notification for {self.user.user.username}: {self.title}"


class SupportMessage(models.Model):
    """Model for storing support/contact messages from users"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='support_messages')
    message = models.TextField(verbose_name='پیام')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال')
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده')
    response = models.TextField(blank=True, verbose_name='پاسخ')
    responded_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ پاسخ')

    class Meta:
        ordering = ['-created_at']
        verbose_name = "پیام پشتیبانی"
        verbose_name_plural = "پیام‌های پشتیبانی"

    def __str__(self):
        return f"Support message from {self.user.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"