from django.contrib import admin
from .models import Design


@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product_id', 'created_at', 'has_preview']
    list_filter = ['created_at', 'user']
    search_fields = ['user__username', 'product_id']
    readonly_fields = ['created_at', 'updated_at', 'design_data_pretty']
    
    fieldsets = (
        ('اطلاعات کلی', {
            'fields': ('user', 'product_id', 'created_at', 'updated_at')
        }),
        ('طراحی', {
            'fields': ('design_data', 'design_data_pretty'),
            'classes': ('wide',)
        }),
        ('پیش‌نمایش', {
            'fields': ('preview_image',)
        }),
    )
    
    def has_preview(self, obj):
        return bool(obj.preview_image)
    has_preview.boolean = True
    has_preview.short_description = 'پیش‌نمایش'
    
    def design_data_pretty(self, obj):
        """نمایش زیبای JSON"""
        import json
        try:
            return json.dumps(obj.design_data, ensure_ascii=False, indent=2)
        except:
            return str(obj.design_data)
    design_data_pretty.short_description = 'مشاهده JSON'
