def cart_total_items(request):
    cart = request.session.get('cart', {})  # دریافت سبد خرید از session

    # بررسی اینکه آیا cart یک دیکشنری است یا نه
    if not isinstance(cart, dict):
        cart = {}  # اگر cart دیکشنری نبود، آن را خالی تنظیم کن

    # محاسبه تعداد کل آیتم‌ها با اطمینان از اینکه هر آیتم دیکشنری است
    total_items = sum(cart.values())

    return {'cart_total_items': total_items}
