# nafis/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class MPTTMeta:
        parent_attr = 'parent'
        order_insertion_by = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Gender(models.Model):
    GENDER_CHOICES = [
        ('مردانه', 'مردانه'),
        ('زنانه', 'زنانه'),
        ('بچگانه', 'بچگانه'),
    ]
    name = models.CharField(max_length=20, choices=GENDER_CHOICES, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "جنسیت"
        verbose_name_plural = "جنسیت‌ها"


class KidsGender(models.Model):
    KIDS_GENDER_CHOICES = [
        ('پسرانه', 'پسرانه'),
        ('دخترانه', 'دخترانه'),
        ('نوزاد پسر', 'نوزاد پسر'),
        ('نوزاد دختر', 'نوزاد دختر'),
        ('مشترک', 'مشترک (پسرانه/دخترانه)'),
    ]
    name = models.CharField(max_length=30, choices=KIDS_GENDER_CHOICES, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "جنسیت بچگانه"
        verbose_name_plural = "جنسیت‌های بچگانه"


class ProductType(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('تی‌شرت', 'تی‌شرت'), ('بلوز', 'بلوز'), ('شلوار', 'شلوار'), ('مانتو', 'مانتو'),
        ('کاپشن', 'کاپشن'), ('شورت', 'شورت'), ('زیرپوش', 'زیرپوش'), ('جوراب', 'جوراب'),
        ('چادر', 'چادر'), ('روسری', 'روسری'), ('مقنعه', 'مقنعه'), ('سرهمی', 'سرهمی'),
        ('پیراهن', 'پیراهن'), ('دامن', 'دامن'), ('کت', 'کت'), ('ژاکت', 'ژاکت'),
        ('هودی', 'هودی'), ('سوئیشرت', 'سوئیشرت'), ('تونیک', 'تونیک'), ('شومیز', 'شومیز'),
        ('لگ', 'لگ'), ('شلوارک', 'شلوارک'), ('کفش', 'کفش'), ('کتانی', 'کتانی'),
        ('صندل', 'صندل'), ('لباس زیر', 'لباس زیر'), ('کلاه', 'کلاه'), ('کیف', 'کیف'),
        ('کمربند', 'کمربند'),
    ]
    name = models.CharField(max_length=50, choices=PRODUCT_TYPE_CHOICES, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "نوع محصول"
        verbose_name_plural = "انواع محصول"


class Style(models.Model):
    STYLE_CHOICES = [
        ('کلاسیک', 'کلاسیک'), ('اسپرت', 'اسپرت'), ('رسمی', 'رسمی'), ('کژوال', 'کژوال'),
        ('مدرن', 'مدرن'), ('وینتیج', 'وینتیج'), ('بوهو', 'بوهو'), ('مینیمال', 'مینیمال'),
        ('شیک', 'شیک'), ('جوانانه', 'جوانانه'), ('کودکانه', 'کودکانه'), ('فانتزی', 'فانتزی'),
        ('ساده', 'ساده'), ('طرح‌دار', 'طرح‌دار'), ('اتنیک', 'اتنیک'), ('گلدوزی', 'گلدوزی'),
        ('چاپی', 'چاپی'), ('یقه‌دار', 'یقه‌دار'), ('بدون آستین', 'بدون آستین'),
        ('آستین بلند', 'آستین بلند'),
    ]
    name = models.CharField(max_length=50, choices=STYLE_CHOICES, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "سبک"
        verbose_name_plural = "سبک‌ها"


class Color(models.Model):
    COLOR_CHOICES = [
        ('مشکی', 'مشکی'), ('سفید', 'سفید'), ('آبی', 'آبی'), ('قرمز', 'قرمز'),
        ('سبز', 'سبز'), ('زرد', 'زرد'), ('نارنجی', 'نارنجی'), ('بنفش', 'بنفش'),
        ('صورتی', 'صورتی'), ('قهوه‌ای', 'قهوه‌ای'), ('خاکستری', 'خاکستری'), ('کرم', 'کرم'),
        ('طلایی', 'طلایی'), ('نقره‌ای', 'نقره‌ای'), ('آبی تیره', 'آبی تیره'),
        ('سبز تیره', 'سبز تیره'), ('قرمز تیره', 'قرمز تیره'), ('بژ', 'بژ'),
        ('فیروزه‌ای', 'فیروزه‌ای'), ('یاسی', 'یاسی'),
    ]
    name = models.CharField(max_length=30, choices=COLOR_CHOICES, unique=True)
    hex_code = models.CharField(max_length=7, blank=True, null=True, help_text="کد رنگ هگزا")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ‌ها"


class Material(models.Model):
    MATERIAL_CHOICES = [
        ('نخی', 'نخی'), ('پشمی', 'پشمی'), ('ابریشمی', 'ابریشمی'), ('کتان', 'کتان'),
        ('پلی‌استر', 'پلی‌استر'), ('ویسکوز', 'ویسکوز'), ('لایکرا', 'لایکرا'), ('جین', 'جین'),
        ('کردروی', 'کردروی'), ('مخمل', 'مخمل'), ('چرم', 'چرم'), ('چرم مصنوعی', 'چرم مصنوعی'),
        ('کشمیر', 'کشمیر'), ('فلیس', 'فلیس'), ('نایلون', 'نایلون'), ('رایون', 'رایون'),
        ('کرپ', 'کرپ'), ('ژاکارد', 'ژاکارد'), ('ترگال', 'ترگال'), ('مخلوط', 'مخلوط'),
    ]
    name = models.CharField(max_length=50, choices=MATERIAL_CHOICES, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "جنس"
        verbose_name_plural = "اجناس"


class Apparel(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='apparels')
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    code = models.CharField(max_length=10, unique=True, blank=True, verbose_name="کد محصول", help_text="این فیلد به صورت خودکار تولید می‌شود.")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    price = models.PositiveIntegerField(verbose_name="قیمت (تومان)")
    
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, verbose_name="جنسیت")
    kids_gender = models.ForeignKey(KidsGender, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="جنسیت بچگانه")
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="نوع محصول")
    style = models.ManyToManyField(Style, blank=True, verbose_name="سبک")
    color = models.ManyToManyField(Color, blank=True, verbose_name="رنگ")
    
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="جنس")
    main_image = models.ImageField(upload_to='apparel_images/main/', blank=True, null=True, verbose_name="تصویر اصلی")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد")

    def save(self, *args, **kwargs):
        # 1. تولید کد محصول به صورت افزایشی از 1001 (در صورت خالی بودن)
        if not self.code:
            last_apparel = Apparel.objects.all().order_by('id').last()
            if last_apparel and last_apparel.code and last_apparel.code.isdigit():
                new_code = int(last_apparel.code) + 1
                self.code = str(new_code)
            else:
                self.code = "1001"  # کد برای اولین محصول

        # 2. تولید slug با فرمت جدید (در صورت خالی بودن)
        if not self.slug:
            gender_map = {'مردانه': 'men', 'زنانه': 'women', 'بچگانه': 'kids'}
            gender_slug = gender_map.get(self.gender.name, slugify(self.gender.name))

            product_slug = "product" # مقدار پیش‌فرض اگر نوع محصول انتخاب نشده باشد
            if self.product_type:
                product_slug = slugify(self.product_type.name)

            self.slug = f"{gender_slug}-{product_slug}-{self.code}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - ({self.code})"

    def get_discounted_price(self):
        active_discount = self.discounts.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now()).first()
        if active_discount:
            discount_amount = (self.price * active_discount.discount_percentage) / 100
            return int(self.price - discount_amount)
        return self.price

    def has_discount(self):
        return self.discounts.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now()).exists()

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"


class Inventory(models.Model):
    apparel = models.ForeignKey(Apparel, on_delete=models.CASCADE, related_name='inventory', verbose_name="محصول")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name="سایز")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name="رنگ")
    quantity = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        unique_together = ('apparel', 'size', 'color')
        verbose_name = "موجودی انبار"
        verbose_name_plural = "موجودی‌های انبار"

    def __str__(self):
        return f"{self.apparel.name} - سایز: {self.size.name} - رنگ: {self.color.name} - موجودی: {self.quantity}"


class ApparelImage(models.Model):
    apparel = models.ForeignKey(Apparel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='apparel_images/multiple/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.apparel.name}"


class SlideShow(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='slideshow_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else f"اسلاید {self.id}"


class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    description = models.TextField(verbose_name="توضیحات")
    image = models.ImageField(upload_to='announcement_images/', verbose_name="تصویر")
    link = models.URLField(blank=True, null=True, verbose_name="لینک (اختیاری)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "اطلاعیه"
        verbose_name_plural = "اطلاعیه‌ها"
        ordering = ['-created_at']


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apparel = models.ForeignKey(Apparel, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.apparel.name} (کاربر: {self.user.username})"

    class Meta:
        unique_together = ('user', 'apparel', 'size', 'color')


class Discount(models.Model):
    apparel = models.ForeignKey(Apparel, on_delete=models.CASCADE, related_name='discounts', verbose_name="محصول")
    discount_percentage = models.PositiveIntegerField(verbose_name="درصد تخفیف")
    start_date = models.DateTimeField(verbose_name="تاریخ شروع")
    end_date = models.DateTimeField(verbose_name="تاریخ پایان")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return f"{self.discount_percentage}% تخفیف برای {self.apparel.name}"

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    class Meta:
        verbose_name = "تخفیف"
        verbose_name_plural = "تخفیف‌ها"


class Order(models.Model):
    STATUS_CHOICES = [
        ('در حال پردازش', 'در حال پردازش'),
        ('ارسال شده', 'ارسال شده'),
        ('تحویل شده', 'تحویل شده'),
        ('لغو شده', 'لغو شده'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(verbose_name="قیمت کل")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='در حال پردازش')

    def __str__(self):
        return f"سفارش #{self.id} توسط {self.user.username}"

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    apparel = models.ForeignKey(Apparel, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField(verbose_name="قیمت")

    def __str__(self):
        return f"{self.quantity} x {self.apparel.name}"