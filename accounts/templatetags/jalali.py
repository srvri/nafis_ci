from django import template
import jdatetime

register = template.Library()

@register.filter
def to_jalali(gregorian_date):
    """
    تبدیل تاریخ میلادی به شمسی (جلالی)
    """
    if not gregorian_date:
        return ""
    
    try:
        # تبدیل تاریخ میلادی به شمسی
        jalali_date = jdatetime.date.fromgregorian(date=gregorian_date)
        # بازگشت به فرمت YYYY-MM-DD
        return jalali_date.strftime('%Y-%m-%d')
    except:
        return gregorian_date

@register.filter
def jalali_display(gregorian_date):
    """
    نمایش تاریخ شمسی به صورت خوانا
    مثال: ۱۴۰۴/۰۹/۱۷
    """
    if not gregorian_date:
        return ""
    
    try:
        jalali_date = jdatetime.date.fromgregorian(date=gregorian_date)
        # تبدیل اعداد انگلیسی به فارسی
        year = str(jalali_date.year)
        month = str(jalali_date.month).zfill(2)
        day = str(jalali_date.day).zfill(2)
        
        # نقشه تبدیل اعداد انگلیسی به فارسی
        persian_digits = {
            '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
            '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'
        }
        
        # تبدیل اعداد
        year = ''.join(persian_digits.get(d, d) for d in year)
        month = ''.join(persian_digits.get(d, d) for d in month)
        day = ''.join(persian_digits.get(d, d) for d in day)
        
        return f"{year}/{month}/{day}"
    except:
        return gregorian_date
