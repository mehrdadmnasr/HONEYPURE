from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

# urls.py in your app (e.g., cart or main app)
urlpatterns = [
    path('cart_detail', views.cart_detail, name='cart_detail'),
    # View to display the cart
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # View to add an item to the cart
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    # View to remove an item from the cart
    path('update/<int:product_id>/', views.update_cart, name='update_cart'),
    # View to update the quantity of an item in the cart
    path('apply_coupon', login_required(views.apply_coupon), name='apply_coupon'),
    # View to apply a coupon to the cart (requires login)
    path('add_address', login_required(views.add_address), name='add_address'),
    # View to add address (requires login)
    path('set_default_address', login_required(views.set_default_address), name='set_default_address'),
    # View to set default address (requires login)
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    # View to delete address (requires login)
    path('checkout', login_required(views.checkout), name='checkout'),
    # View to proceed to checkout (requires login)
    path('payment', login_required(views.payment), name='payment'),
    # View to handle the payment (requires login)
    path('process_payment', login_required(views.process_payment), name='process_payment'),
    # Process payment (requires login)
    path('paypal_payment', login_required(views.paypal_payment), name='paypal_payment'),
    # PayPal payment (requires login)
    path('paypal_return', login_required(views.paypal_return), name='paypal_return'),
    # PayPal return (requires login)
    path('paypal_cancel', views.paypal_cancel, name='paypal_cancel'),
    # PayPal cancel (requires login)
]
