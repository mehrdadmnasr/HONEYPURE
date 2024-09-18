from django.contrib import admin
from .models import Tax, Cart, CartItem, Order, OrderItem, Address, AvailableSlot, Coupon

# تنظیم صفحه ادمین برای مدل Coupon
@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['year', 'tax_percentage', 'toll_percentage']
    search_fields = ['year']
    list_filter = ['year']

# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_name', 'address_line1', 'city', 'country', 'location_lat', 'location_long', 'default')
    search_fields = ('address_name', 'address_line1', 'city', 'country')
    list_filter = ('default', 'city', 'country')
    readonly_fields = ('user',)  # به دلخواه می‌توانید فیلدهای غیرقابل ویرایش را تنظیم کنید

# تنظیم صفحه ادمین برای مدل Cart
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'coupon', 'get_total_items']
    search_fields = ['user__username']
    list_filter = ['created_at', 'coupon']

    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Total Items'

# تنظیم صفحه ادمین برای مدل CartItem
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
    search_fields = ['cart__user__username', 'product__product_title']
    list_filter = ['cart']

# تنظیم صفحه ادمین برای مدل Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'status', 'paid', 'tracking_number']
    search_fields = ['user__username', 'tracking_number', 'email']
    list_filter = ['created_at', 'status', 'paid']

# تنظیم صفحه ادمین برای مدل OrderItem
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    search_fields = ['order__user__username', 'product__product_title']
    list_filter = ['order']

# تنظیم صفحه ادمین برای مدل AvailableSlot
@admin.register(AvailableSlot)
class AvailableSlotAdmin(admin.ModelAdmin):
    list_display = ['date', 'time_start', 'time_end', 'is_available']
    list_filter = ['date', 'is_available']

# تنظیم صفحه ادمین برای مدل Coupon
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_amount', 'valid_from', 'valid_to', 'active']
    search_fields = ['code']
    list_filter = ['valid_from', 'valid_to', 'active']
