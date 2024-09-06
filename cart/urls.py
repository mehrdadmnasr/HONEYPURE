from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

# urls.py in your app (e.g., cart or main app)
urlpatterns = [
    # View to display the cart
    path('cart_detail', views.cart_detail, name='cart_detail'),
    # View to add an item to the cart
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # View to remove an item from the cart
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    # View to update the quantity of an item in the cart
    path('update/<int:product_id>/', views.update_cart, name='update_cart'),
    # View to apply a coupon to the cart (requires login)
    path('apply_coupon', login_required(views.apply_coupon), name='apply_coupon'),
    # View to manage addresses (requires login)
    path('manage_addresses', login_required(views.manage_addresses), name='manage_addresses'),
    # View to proceed to checkout (requires login)
    path('checkout', login_required(views.checkout), name='checkout'),
    # View to handle the payment (requires login)
    path('payment', login_required(views.payment), name='payment'),
    # Process payment (requires login)
    path('process_payment', login_required(views.process_payment), name='process_payment'),
    # PayPal payment (requires login)
    path('paypal_payment', login_required(views.paypal_payment), name='paypal_payment'),
    # PayPal return (requires login)
    path('paypal_return', login_required(views.paypal_return), name='paypal_return'),
    # PayPal cancel (requires login)
    path('paypal_cancel', views.paypal_cancel, name='paypal_cancel'),
]
