from django.core.management.base import BaseCommand
from nafis.models import Gender, KidsGender, ProductType, Style, Color, Material, Size


class Command(BaseCommand):
    help = 'پر کردن داده‌های اولیه برای مدل‌ها'

    def handle(self, *args, **options):
        self.stdout.write('شروع پر کردن داده‌های اولیه...')

        # ایجاد جنسیت‌ها
        genders = ['مردانه', 'زنانه', 'بچگانه']
        for gender_name in genders:
            gender, created = Gender.objects.get_or_create(name=gender_name)
            if created:
                self.stdout.write(f'جنسیت "{gender_name}" ایجاد شد.')

        # ایجاد جنسیت‌های بچگانه
        kids_genders = ['پسرانه', 'دخترانه', 'نوزاد', 'مشترک']
        for kids_gender_name in kids_genders:
            kids_gender, created = KidsGender.objects.get_or_create(name=kids_gender_name)
            if created:
                self.stdout.write(f'جنسیت بچگانه "{kids_gender_name}" ایجاد شد.')

        # ایجاد انواع محصول
        product_types = [
            'تی‌شرت', 'بلوز', 'شلوار', 'مانتو', 'کاپشن', 'شورت', 'زیرپوش',
            'جوراب', 'چادر', 'روسری', 'مقنعه', 'سرهمی', 'پیراهن', 'دامن',
            'کت', 'ژاکت', 'هودی', 'سوئیشرت', 'تونیک', 'شومیز', 'لگ',
            'شلوارک', 'کفش', 'کتانی', 'صندل', 'لباس زیر', 'کلاه', 'کیف', 'کمربند'
        ]
        for product_type_name in product_types:
            product_type, created = ProductType.objects.get_or_create(name=product_type_name)
            if created:
                self.stdout.write(f'نوع محصول "{product_type_name}" ایجاد شد.')

        # ایجاد سبک‌ها
        styles = [
            'کلاسیک', 'اسپرت', 'رسمی', 'کژوال', 'مدرن', 'وینتیج', 'بوهو',
            'مینیمال', 'شیک', 'جوانانه', 'کودکانه', 'فانتزی', 'ساده',
            'طرح‌دار', 'اتنیک', 'گلدوزی', 'چاپی', 'یقه‌دار', 'بدون آستین', 'آستین بلند'
        ]
        for style_name in styles:
            style, created = Style.objects.get_or_create(name=style_name)
            if created:
                self.stdout.write(f'سبک "{style_name}" ایجاد شد.')

        # ایجاد رنگ‌ها
        colors_data = [
            ('مشکی', '#000000'),
            ('سفید', '#FFFFFF'),
            ('آبی', '#0066FF'),
            ('قرمز', '#FF0000'),
            ('سبز', '#00FF00'),
            ('زرد', '#FFFF00'),
            ('نارنجی', '#FF8000'),
            ('بنفش', '#8000FF'),
            ('صورتی', '#FF69B4'),
            ('قهوه‌ای', '#8B4513'),
            ('خاکستری', '#808080'),
            ('کرم', '#F5F5DC'),
            ('طلایی', '#FFD700'),
            ('نقره‌ای', '#C0C0C0'),
            ('آبی تیره', '#000080'),
            ('سبز تیره', '#006400'),
            ('قرمز تیره', '#8B0000'),
            ('بژ', '#F5F5DC'),
            ('فیروزه‌ای', '#40E0D0'),
            ('یاسی', '#DA70D6'),
        ]
        for color_name, hex_code in colors_data:
            color, created = Color.objects.get_or_create(
                name=color_name,
                defaults={'hex_code': hex_code}
            )
            if created:
                self.stdout.write(f'رنگ "{color_name}" ایجاد شد.')

        # ایجاد مواد (جنس‌ها)
        materials = [
            'نخی', 'پشمی', 'ابریشمی', 'کتان', 'پلی‌استر', 'ویسکوز',
            'لایکرا', 'جین', 'کردروی', 'مخمل', 'چرم', 'چرم مصنوعی',
            'کشمیر', 'فلیس', 'نایلون', 'رایون', 'کرپ', 'ژاکارد', 'ترگال', 'مخلوط'
        ]
        for material_name in materials:
            material, created = Material.objects.get_or_create(name=material_name)
            if created:
                self.stdout.write(f'جنس "{material_name}" ایجاد شد.')

        # ایجاد سایزها
        sizes = [
            'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL',  # سایزهای بزرگسالان
            '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46',  # سایزهای کفش
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',  # سایزهای بچگانه
            'نوزاد', 'یک ساله', 'دو ساله', 'سه ساله', 'چهار ساله', 'پنج ساله'
        ]
        for size_name in sizes:
            size, created = Size.objects.get_or_create(name=size_name)
            if created:
                self.stdout.write(f'سایز "{size_name}" ایجاد شد.')

        self.stdout.write(self.style.SUCCESS('تمام داده‌های اولیه با موفقیت ایجاد شدند!'))