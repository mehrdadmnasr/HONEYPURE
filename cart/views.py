from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tax, Cart, CartItem, Order, OrderItem, Address, Coupon, AvailableSlot
from products.models import Product
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.conf import settings
from .forms import AddressForm
from collections import defaultdict
import paypalrestsdk

def get_cart(request):
    return request.session.get('cart', {})

def save_cart(request, cart):
    request.session['cart'] = cart

def update_after_edit_cart(request, cart):
    # به‌روزرسانی اطلاعات سبد خرید پس از ویرایش
    total_items = sum(cart.values())  # جمع کل تعداد اقلام

    # Fetch tax information
    current_year = timezone.now().year
    tax_info = get_object_or_404(Tax, year=current_year)

    # محاسبه قیمت کل
    total_price = 0
    for pid, quantity in cart.items():
        product = get_object_or_404(Product, id=int(pid))
        item_price = float(product.price) * quantity
        tax = item_price * (float(tax_info.tax_percentage) / 100)
        toll = item_price * (float(tax_info.toll_percentage) / 100)
        total_price += item_price + tax + toll
        # ذخیره تعداد کل اقلام و قیمت کل در سشن

    # Convert to float before storing in session
    request.session['total_price'] = float(total_price)
    request.session['total_items'] = total_items

    # Optionally, reapply the coupon if one is present
    if request.session.get('coupon_code'):
        apply_coupon_logic(request)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
#    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 1)) # دریافت تعداد از فرم
    # افزودن به سبد خرید یا افزایش مقدار
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity

    save_cart(request, cart)
    # به‌روزرسانی اطلاعات سبد خرید
    update_after_edit_cart(request, cart)

    return redirect('cart_detail')

def cart_detail(request):
    cart = get_cart(request)
    #cart = request.session.get('cart', {})
    items = [] # اگر کاربر وارد نشده باشد، آیتم‌ها باید خالی باشند
    total_price = 0
    total_items = sum(cart.values())
    current_year = timezone.now().year  # Get the current year for tax info

    # Fetch tax information based on the current year
    tax_info = get_object_or_404(Tax, year=current_year)

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        item_price = float(product.price) * quantity

        # Calculate tax and toll
        tax = item_price * (float(tax_info.tax_percentage) / 100)
        toll = item_price * (float(tax_info.toll_percentage) / 100)
        item_total = item_price + tax + toll

        item = {
            'product': product,
            'quantity': quantity,
            'unit_price': float(product.price),  # Unit price
            'item_price': item_price,            # Price before tax and toll
            'tax': tax,                          # Calculated tax
            'toll': toll,                        # Calculated toll
            'total_price': item_total            # Total price including tax and toll
        }
        items.append(item)
        total_price += item['total_price']  # Accumulate total price for all items

    # Recalculate the discount
    discount_amount = float(request.session.get('discount_amount', 0))
    coupon_code = request.session.get('coupon_code', None)

    # Final price after applying discount
    final_price = total_price - discount_amount

    data = {
        'items': items,
        'total_price': total_price,
        'final_price': final_price,
        'discount_amount': discount_amount,
        'total_items': total_items,
        'coupon_code': coupon_code
    }

    return render(request, 'cart/cart_detail.html', data)

def remove_from_cart(request, product_id):
    cart = get_cart(request)
    cart.pop(str(product_id), None)
    save_cart(request, cart)
    # به‌روزرسانی اطلاعات سبد خرید
    update_after_edit_cart(request, cart)

    return redirect('cart_detail')

def update_cart(request, product_id):
    cart = get_cart(request)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            cart.pop(str(product_id), None)
    save_cart(request, cart)
    # به‌روزرسانی اطلاعات سبد خرید
    update_after_edit_cart(request, cart)

    return redirect('cart_detail')

@login_required(login_url='/accounts/login/')
def checkout(request):
    if request.method == 'POST':
        address_id = request.POST.get('selected_address')
        slot_id = request.POST.get('selected_slot')  # دریافت اسلات انتخاب شده

        if not address_id:
            messages.error(request, 'Please select an address.')
            return redirect('checkout')

        if not slot_id:  # بررسی اینکه اسلات زمانی انتخاب شده است یا خیر
            messages.error(request, 'Please select a time slot.')
            return redirect('checkout')

        # گرفتن آدرس انتخاب شده توسط کاربر
        address = get_object_or_404(Address, id=address_id, user=request.user)
        # گرفتن اسلات انتخاب شده توسط کاربر
        slot = get_object_or_404(AvailableSlot, id=slot_id)
        # گرفتن سبد خرید کاربر
        cart = Cart.objects.get(user=request.user)

        # ایجاد سفارش جدید
        order = Order.objects.create(
            user=request.user,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            email=request.user.email,
            address=address,
            paid=False,
            status='Processing',
            delivery_date=slot.date,
            delivery_time=f"{slot.time_start} - {slot.time_end}"
        )

        # ایجاد آیتم‌های سفارش از سبد خرید
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
            item.delete()  # حذف آیتم از سبد خرید پس از ایجاد سفارش

        cart.delete()  # حذف سبد خرید پس از تکمیل سفارش
        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_summary', order_id=order.id)

    else:
        # آدرس‌های کاربر و اسلات‌های زمانی قابل دسترسی
        addresses = Address.objects.filter(user=request.user)
        available_slots = AvailableSlot.objects.order_by('date')

        # Group available slots by date
        grouped_slots = {}
        for slot in available_slots:
            if slot.date not in grouped_slots:
                grouped_slots[slot.date] = []
            grouped_slots[slot.date].append(slot)

        # پیدا کردن آدرس پیش‌فرض
        default_address = addresses.filter(default=True).first()

        # داده‌ها برای نمایش در صفحه checkout
        data = {
            'addresses': addresses,
            'grouped_slots': grouped_slots,  # ارسال اسلات‌ها به صورت گروه‌بندی‌شده
            'selected_address': default_address,
        }
        return render(request, 'cart/checkout.html', data)

@login_required(login_url='/accounts/login/')
def set_default_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        address = get_object_or_404(Address, id=address_id, user=request.user)

        # حذف پیش‌فرض بودن از سایر آدرس‌ها
        Address.objects.filter(user=request.user).update(default=False)

        # تنظیم آدرس انتخاب شده به عنوان پیش‌فرض
        address.default = True
        address.save()

        messages.success(request, 'Address set as default.')
        return redirect('checkout')

@login_required(login_url='/accounts/login/')
def delete_address(request, address_id):
    if request.method == 'POST':
        #address_id = request.POST.get('address_id')
        address = get_object_or_404(Address, id=address_id, user=request.user)

        # حذف آدرس
        address.delete()

        messages.success(request, 'Address deleted.')
        return redirect('checkout')

@login_required(login_url='/accounts/login/')
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address added successfully.')
            return redirect('checkout')  # یا هر ویویی که بعد از افزودن آدرس می‌خواهید کاربر به آن هدایت شود
    else:
        form = AddressForm(user=request.user)
    return render(request, 'cart/add_address.html', {'form': form})

def apply_coupon_logic(request):
    code = request.session.get('coupon_code')
    if not code:
        return

    try:
        coupon = Coupon.objects.get(code=code, active=True)
    except Coupon.DoesNotExist:
        # Invalid coupon, remove from session
        request.session['discount_amount'] = 0
        request.session['coupon_code'] = None
        return

    total_price = request.session.get('total_price', 0)
    discount_amount = float(coupon.discount_amount)

    if discount_amount > (total_price / 2):
        discount_amount = total_price / 2
        # Add warning message if discount is capped at 50%
        messages.warning(request, "The maximum discount is 50% of the total cart value.")

    # Store the discount amount in the session
    request.session['discount_amount'] = discount_amount

@login_required
def apply_coupon(request):
    if request.method == "POST":
        code = request.POST.get('coupon_code')
        request.session['coupon_code'] = code
        apply_coupon_logic(request)
        messages.success(request, f"Coupon {code} applied successfully!")
        return redirect('cart_detail')
    return redirect('cart_detail')

#توضیحات تغییرات:
# Initialize PayPal SDK
paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

@login_required
def payment(request):
    """Render the payment page where users can select a payment method."""
    # بررسی اینکه آیا آدرس و اسلات زمانی انتخاب شده‌اند
    selected_address_id = request.session.get('selected_address_id')
    selected_slot_id = request.session.get('selected_slot_id')

    if not selected_address_id or not selected_slot_id:
        messages.error(request, 'Please complete the checkout process first.')
        return redirect('checkout')

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
