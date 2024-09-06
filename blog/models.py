from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField

class Blog(models.Model):
    title = models.CharField(max_length=255)  # عنوان بلاگ
    author = models.CharField(max_length=255)  # نام نویسنده
    image = models.ImageField(upload_to='blogs/%Y/%m/%d/')  # تصویر بلاگ
    summary = RichTextField()  # خلاصه بلاگ
    content = RichTextField()  # محتوای بلاگ
    tags = models.JSONField(default=list, blank=True, null=True)  # تگ‌های بلاگ به صورت لیست
    publish_date = models.DateTimeField(default=datetime.now, blank=True)  # تاریخ نشر
    update_date = models.DateTimeField(auto_now=True)  # تاریخ ویرایش
    version = models.PositiveIntegerField(default=1)  # شماره ویرایش

    def __str__(self):
        return self.title  # نمایش عنوان بلاگ به عنوان رشته
