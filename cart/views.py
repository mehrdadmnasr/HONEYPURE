from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem, Address, Coupon
from products.models import Product
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.conf import settings
import paypalrestsdk

def get_cart(request):
#    if request.user.is_authenticated:
#        return Cart.objects.get_or_create(user=request.user)[0]
#    else:
        return request.session.get('cart', {})

def save_cart(request, cart):
#    if request.user.is_authenticated:
#        cart_instance, created = Cart.objects.get_or_create(user=request.user)
#        for product_id, quantity in cart.items():
#            product = get_object_or_404(Product, id=product_id)
#            cart_item, created = CartItem.objects.get_or_create(cart=cart_instance, product=product)
#            cart_item.quantity = quantity
#            cart_item.save()
#        request.session.pop('cart', None)
#    else:
        request.session['cart'] = cart

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
#    if request.user.is_authenticated:
#        cart = Cart.objects.get_or_create(user=request.user)[0]
#        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#        if not created:
#            cart_item.quantity += 1
#        cart_item.save()
#    else:

    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 1)) # دریافت تعداد از فرم

    # افزودن به سبد خرید یا افزایش مقدار
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity

    save_cart(request, cart)
    return redirect('cart_detail')

def cart_detail(request):
#    if request.user.is_authenticated:
#        cart = Cart.objects.get(user=request.user)
#        items = CartItem.objects.filter(cart=cart)
#            # تمام آیتم‌های سبد خرید را دریافت کنید items = cart.items.all()
#        data = {
#            'cart': cart,
#            'items': items,
#            'total_price': cart.get_total_price(),
#            'total_items': cart.get_total_items(),
#        }
#    else:
    cart = request.session.get('cart', {})

    items = [] # اگر کاربر وارد نشده باشد، آیتم‌ها باید خالی باشند

    total_price = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        item = {
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        }
        items.append(item)
        total_price += item['total_price']

#    total_price = sum(Product.objects.get(id=int(prod_id)).price * qty for prod_id, qty in cart.items())
    data = {
        'items': items,
        'total_price': total_price,
        'total_items': sum(cart.values()),
    }
    return render(request, 'cart/cart_detail.html', data)

def remove_from_cart(request, product_id):
#    if request.user.is_authenticated:
#        cart_item = get_object_or_404(CartItem, id=product_id)
#        cart_item.delete()
#    else:
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    save_cart(request, cart)

    return redirect('cart_detail')

def update_cart(request, product_id):
#    if request.user.is_authenticated:
#        cart_item = get_object_or_404(CartItem, id=product_id)
#        if request.method == 'POST':
#            quantity = int(request.POST.get('quantity', 1))
#            if quantity > 0:
#                cart_item.quantity = quantity
#                cart_item.save()
#            else:
#                cart_item.delete()
#    else:
    cart = request.session.get('cart', {})
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            cart.pop(str(product_id), None)
        save_cart(request, cart)

    # محاسبه مقدار کل سطر برای محصول به‌روزرسانی‌شده
    product = get_object_or_404(Product, id=int(product_id))
    total_price_for_item = product.price * cart[str(product_id)]
    print(f"Updated Total Price for Product {product.product_title}: {total_price_for_item}")

    return redirect('cart_detail')

@login_required(login_url='/accounts/login/')
def checkout(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in first.')
        return redirect(f"{reverse('login')}?next={request.path}")

    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        address = get_object_or_404(Address, id=address_id, user=request.user)
        cart = Cart.objects.get(user=request.user)

        order = Order.objects.create(
            user=request.user,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            email=request.user.email,
            address=address,
            paid=False,
            status='Processing'
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
            item.delete()

        cart.delete()

        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_summary', order_id=order.id)

    else:
        addresses = Address.objects.filter(user=request.user)
        data = {
            'addresses': addresses,
        }
        return render(request, 'cart/checkout.html', data)

@login_required
def manage_addresses(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            Address.objects.create(
                user=request.user,
                address_line1=request.POST.get('address_line1'),
                address_line2=request.POST.get('address_line2'),
                city=request.POST.get('city'),
                postal_code=request.POST.get('postal_code'),
                country=request.POST.get('country'),
                phone_number=request.POST.get('phone_number'),
                location_lat=request.POST.get('location_lat'),
                location_long=request.POST.get('location_long'),
                default=request.POST.get('default', False)
            )
        elif action == 'update':
            address_id = request.POST.get('address_id')
            address = get_object_or_404(Address, id=address_id, user=request.user)
            address.address_line1 = request.POST.get('address_line1')
            address.address_line2 = request.POST.get('address_line2')
            address.city = request.POST.get('city')
            address.postal_code = request.POST.get('postal_code')
            address.country = request.POST.get('country')
            address.phone_number = request.POST.get('phone_number')
            address.location_lat = request.POST.get('location_lat')
            address.location_long = request.POST.get('location_long')
            address.default = request.POST.get('default', False)
            address.save()
        elif action == 'delete':
            address_id = request.POST.get('address_id')
            address = get_object_or_404(Address, id=address_id, user=request.user)
            address.delete()

    addresses = Address.objects.filter(user=request.user)
    data = {
        'addresses': addresses,
    }
    return render(request, 'cart/manage_addresses.html', data)

@login_required
def apply_coupon(request):
    if request.method == "POST":
        code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code=code, active=True)
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon code")
            return redirect('cart_detail')

        cart = Cart.objects.get(user=request.user)

        cart.coupon = coupon
        cart.save()

        messages.success(request, f"Coupon {code} applied successfully!")
        return redirect('cart_detail')

    return redirect('cart_detail')

# Initialize PayPal SDK
paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

@login_required
def payment(request):
    """Render the payment page where users can select a payment method."""
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        if payment_method:
            # Redirect to payment processing based on the selected method
            return redirect(reverse('process_payment'))
        else:
            messages.error(request, "Please select a payment method.")
    return render(request, 'cart/payment.html')

@require_POST
@login_required
def process_payment(request):
    """Handle payment processing based on the selected method."""
    payment_method = request.POST.get('payment_method')

    if payment_method == 'paypal':
        return redirect(reverse('paypal_payment'))
    elif payment_method == 'credit_card':
        # Implement credit card payment logic here
        pass
    elif payment_method == 'bank_transfer':
        # Implement bank transfer logic here
        pass
    else:
        messages.error(request, "Invalid payment method.")
        return redirect(reverse('payment'))

@login_required
def process_payment(request):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('paypal_return')),
            "cancel_url": request.build_absolute_uri(reverse('paypal_cancel'))
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Your Order",
                    "sku": "item",
                    "price": str(total_price),  # جمع کل واقعی را اینجا قرار دهید
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(total_price),  # جمع کل واقعی را اینجا قرار دهید
                "currency": "USD"
            },
            "description": "This is the payment description."
        }]
    })

    if payment.create():
        approval_url = next(link.href for link in payment.links if link.rel == "approval_url")
        return redirect(approval_url)
    else:
        messages.error(request, "Failed to create PayPal payment.")
        return redirect(reverse('payment'))

@login_required
def paypal_payment(request):
    """Handle the PayPal payment process."""
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('payment_success')),
            "cancel_url": request.build_absolute_uri(reverse('paypal_cancel')),
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Your Order",
                    "sku": "item",
                    "price": "10.00",  # باید قیمت واقعی را اینجا قرار دهید
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": "10.00",  # باید مجموع مبلغ واقعی را اینجا قرار دهید
                "currency": "USD"
            },
            "description": "Payment for your order."
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = link.href
                return redirect(approval_url)
    else:
        print(payment.error)
        return redirect(reverse('payment_failed'))

    return redirect(reverse('payment'))


@login_required
def paypal_return(request):
    """Handle PayPal payment return after user approves the payment."""
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        messages.success(request, "Payment was successful.")
        return redirect(reverse('order_confirmation'))
    else:
        messages.error(request, "Payment failed.")
        return redirect(reverse('payment'))

@login_required
def paypal_cancel(request):
    """Handle PayPal payment cancellation."""
    messages.info(request, "Payment was cancelled.")
    return redirect(reverse('payment'))
