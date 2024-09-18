from django.contrib.auth import get_user_model
from django.db import models
from products.models import Product  # اطمینان از مسیر صحیح
from django.utils import timezone

User = get_user_model()

class Tax(models.Model):
    year = models.PositiveIntegerField(default=timezone.now().year)  # ذخیره سال
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    toll_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Year: {self.year}, Tax: {self.tax_percentage}%, Toll: {self.toll_percentage}%"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The user who owns this cart
    created_at = models.DateTimeField(auto_now_add=True)
    # Date and time when the cart was created
    coupon = models.ForeignKey('Coupon', null=True, blank=True, on_delete=models.SET_NULL)
    # Optional: A coupon that can be applied to this cart

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_total_price(self):
        total = sum(item.get_total_price_with_tax() for item in self.items.all())
        if self.coupon:
            max_discount = total / 2  # تخفیف حداکثر نصف جمع کل
            discount = min(self.coupon.discount_amount, max_discount)
            total -= discount
        return total

    def get_total_items(self):
        return self.items.count()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    # The cart that this item belongs to
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    # The product that is being added to the cart
    quantity = models.PositiveIntegerField(default=1)
    # The quantity of the product in the cart
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # درصد مالیات
    toll_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # درصد عوارض

    def __str__(self):
        return f"{self.quantity} x {self.product.product_title}"

    def get_total_price(self):
        return self.product.price * self.quantity

    def get_total_price_with_tax(self):
        total_price = self.get_total_price()
        tax_amount = total_price * (self.tax_percent / 100)
        toll_amount = total_price * (self.toll_percent / 100)
        return total_price + tax_amount + toll_amount

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # The user who placed this order
    first_name = models.CharField(max_length=100)
    # The first name of the user
    last_name = models.CharField(max_length=100)
    # The last name of the user
    email = models.EmailField()
    # The email of the user for communication
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True)
    # The address where the order should be delivered
    created_at = models.DateTimeField(auto_now_add=True)
    # The date and time when the order was created
    updated_at = models.DateTimeField(auto_now=True)
    # The date and time when the order was last updated
    paid = models.BooleanField(default=False)
    # Whether the order has been paid for
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    # The tracking number for the order (optional)
    status = models.CharField(max_length=20, default='Processing')
    # The current status of the order (e.g., Processing, Shipped, Delivered)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def get_total_price(self):
        # Calculate the total price of the order
        total = sum(item.get_total_price() for item in self.items.all())
        if self.cart.coupon:
            total -= (total * (self.cart.coupon.discount / 100))  # Apply discount if a coupon is available
        return total

    def get_total_price(self):
        total = sum(item.get_total_price() for item in self.items.all())
        return total - self.get_discount()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # The order that this item belongs to
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # The product that is included in the order
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # The price of the product at the time of the order
    quantity = models.PositiveIntegerField(default=1)
    # The quantity of the product ordered

    def __str__(self):
        return f"{self.quantity} x {self.product.product_title}"

    def get_total_price(self):
        # Calculate the total price for this item (quantity * price)
        return self.quantity * self.price

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # The user who owns this address
    address_name = models.CharField(max_length=100, blank=False, null=False, default='')  # فیلد اجباری  # نام آدرس
    # The name of the address
    address_details = models.TextField(blank=False, null=False, default='')
    # Detailed address information (e.g., specific instructions or landmarks)
    address_line1 = models.CharField(max_length=255, blank=False, null=False, default='')  # فیلد اجباری
    # The first line of the address (e.g., street name)
    address_line2 = models.CharField(max_length=255, blank=True, null=True, default='')
    # The second line of the address (e.g., apartment, suite) (optional)
    city = models.CharField(max_length=100, blank=False, null=False, default='')
    # The city of the address
    state = models.CharField(max_length=100, blank=True, null=True, default='')
    # The state or province of the address (optional)
    postal_code = models.CharField(max_length=20, blank=False, null=False, default='')
    # The postal code of the address
    country = models.CharField(max_length=100, blank=False, null=False, default='')
    # The country of the address
    phone_number = models.CharField(max_length=20, blank=True, null=True, default='')
    # The phone number associated with this address (optional)
    mobile_number = models.CharField(max_length=20, blank=False, null=False, default='')
    # The mobile number associated with this address (optional)
    email = models.EmailField(blank=True, null=True, default='')
    # The email address associated with this address (optional)
    location_lat = models.DecimalField(max_digits=22, decimal_places=18, null=False, blank=False, default='')
    # The latitude of the location (from Google Maps)
    location_long = models.DecimalField(max_digits=22, decimal_places=18, null=False, blank=False, default='')
    # The longitude of the location (from Google Maps)
    default = models.BooleanField(default=False)
    # Whether this address is the default address for the user

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.country}"

    class Meta:
        verbose_name_plural = "Addresses"
        # Plural name for the model in the admin interface
        constraints = [
            models.UniqueConstraint(fields=['user', 'address_name'], name='unique_address_name_per_user')
        ]

class AvailableSlot(models.Model):
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.date} from {self.time_start} to {self.time_end}"

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    # The unique code for the coupon
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # The discount that this coupon offers
    valid_from = models.DateTimeField()
    # The date and time from which the coupon is valid
    valid_to = models.DateTimeField()
    # The date and time until which the coupon is valid
    active = models.BooleanField(default=True)
    # Whether the coupon is currently active and can be used

    def __str__(self):
        return f"Coupon {self.code} - {self.discount_amount} off"
