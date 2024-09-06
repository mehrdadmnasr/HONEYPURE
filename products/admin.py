from django.contrib import admin
from .models import Product, ProductReview
from django.utils.html import format_html

class ProductAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.product_photo.url))

    thumbnail.short_description = 'Product Image'
    list_display = ('id', 'thumbnail', 'product_title', 'price', 'sku', 'weight', 'is_new',
        'available', 'stock')
    list_display_links = ('id', 'thumbnail', 'product_title')
    list_editable = ('available',)
    search_fields = ('id', 'product_title', 'price', 'weight', 'available', 'stock')
    list_filter = ('price', 'weight', 'available', 'stock')

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'reviewer_name', 'rating', 'review_date', 'verified_purchase')
    list_filter = ('verified_purchase', 'rating')
    search_fields = ('product__product_title', 'reviewer_name')

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
