from django.db import models
from django.contrib.auth.models import User  # اضافه کردن import برای User
from datetime import datetime
from ckeditor.fields import RichTextField
from multiselectfield import MultiSelectField
from django.conf import settings

class Product(models.Model):
    product_title = models.CharField(max_length=255)  # نام محصول
    description = RichTextField()  # توضیحات محصول با قابلیت قالب‌بندی
    detail = RichTextField(blank=True, null=True)  # جزئیات محصول با قابلیت قالب‌بندی
    price = models.DecimalField(max_digits=10, decimal_places=2)  # قیمت محصول
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # قیمت قبلی محصول (برای تخفیف‌ها)
    sku = models.CharField(max_length=100, unique=True)  # شناسه محصول (SKU)
    stock = models.PositiveIntegerField()  # تعداد موجودی محصول
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # وزن محصول (اختیاری)
    available = models.BooleanField(default=True)  # وضعیت موجودی محصول
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)  # امتیاز محصول
    is_new = models.BooleanField(default=False)  # نشان‌دهنده جدید بودن محصول
    tags = models.CharField(max_length=255, blank=True, null=True)  # تگ‌های محصول (اختیاری)
    created_date = models.DateTimeField(default=datetime.now, blank=True)  # تاریخ و زمان ایجاد محصول
    updated_date = models.DateTimeField(auto_now=True)  # تاریخ و زمان آخرین به‌روزرسانی

    # تصاویر محصول
    product_photo = models.ImageField(upload_to='products/%Y/%m/%d/')  # تصویر اصلی محصول
    product_photo_1 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)  # تصویر دوم محصول (اختیاری)
    product_photo_2 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)  # تصویر سوم محصول (اختیاری)
    product_photo_3 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)  # تصویر چهارم محصول (اختیاری)
    product_photo_4 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)  # تصویر پنجم محصول (اختیاری)

    # ویژگی‌های محصول
    features_choices = (
        ('Natural Ingredients', 'Natural Ingredients'),  # مواد طبیعی
        ('Organic', 'Organic'),  # ارگانیک
        ('Raw Honey', 'Raw Honey'),  # عسل خام
        ('Freshly Harvested', 'Freshly Harvested'),  # تازه برداشت شده
        ('Unprocessed', 'Unprocessed'),  # فرآوری نشده
        ('Premium Quality', 'Premium Quality'),  # کیفیت بالا
        ('No Additives', 'No Additives'),  # بدون افزودنی
    )
    features = MultiSelectField(choices=features_choices, max_length=600, max_choices=10)  # ویژگی‌های محصول

    def __str__(self):
        return self.product_title  # نمایش نام محصول به عنوان رشته

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')  # مرجع به محصول
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who wrote the review
    reviewer_name = models.CharField(max_length=255)  # نام بازبین
    review_text = models.TextField()  # متن بازبینی
    review_date = models.DateField(auto_now_add=True)  # تاریخ بازبینی
    rating = models.PositiveIntegerField(default=5)  # امتیاز بازبینی
    verified_purchase = models.BooleanField(default=False)  # نشان‌دهنده خرید تأیید شده

    def __str__(self):
        return f"Review by {self.user.username} on {self.product.product_title}"
