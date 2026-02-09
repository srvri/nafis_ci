from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Design(models.Model):
    
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='designs'
    )
    
    product_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="شناسه محصول (برای تطبیق آینده با جدول محصولات)"
    )
    
    design_data = models.JSONField(
        default=dict,
        help_text="""
        ساختار طراحی: {
          "version": 1,
          "items": [
            {"image": "...", "x": 0, "y": 0, "scale": 1, "rotation": 0, "z": 0}
          ],
          "activeItemIndex": 0,
          "uvSize": 2048
        }
        """
    )
    
    preview_image = models.ImageField(
        upload_to='designs/previews/%Y/%m/',
        null=True,
        blank=True,
        help_text="تصویر پیش‌نمایش PNG"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'طراحی'
        verbose_name_plural = 'طراحی‌ها'
    
    def __str__(self):
        return f"Design #{self.id} - User: {self.user or 'Anonymous'}"
