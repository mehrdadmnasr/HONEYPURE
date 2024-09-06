from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductReview
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages

# Create your views here.
def products(request):
    products = Product.objects.order_by('-created_date')
    #paginator = Paginator(products, 2) # No of products in each page
    #page = request.GET.get('page')
    #paged_products = paginator.get_page(page)

    data = {
    	#'products': paged_products,
        'products': products,
    }
    return render(request, 'products/products.html', data)

def product_detail(request, id):
    single_product = get_object_or_404(Product, pk=id)

    if request.method == 'POST':
        reviewer_name = request.POST['reviewer_name']
        review_text = request.POST['review_text']
        rating = request.POST['rating']
        verified_purchase = 'verified_purchase' in request.POST

        review = ProductReview(
            product = single_product,
            reviewer_name = reviewer_name,
            review_text = review_text,
            rating = rating,
            verified_purchase = verified_purchase
        )
        review.save()
        messages.success(request, 'بازبینی شما با موفقیت ثبت شد و پس از تأیید نمایش داده خواهد شد.')
        return redirect('product_detail', id=id)

    reviews = single_product.reviews.all()

    # محاسبه میانگین نمرات
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    if average_rating is None:
        average_rating = 5.0  # یا هر مقدار پیش‌فرض دیگری که مدنظر دارید

    data = {
        'single_product' : single_product,
        'reviews': reviews,
        'average_rating': average_rating,  # ارسال میانگین نمرات به قالب
    }
    return render(request, 'products/product_detail.html', data)


def get_product_reviews(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()
    reviews_data = []
    for review in reviews:
        reviews_data.append({
            'reviewer_name': review.reviewer_name,
            'review_text': review.review_text,
            'rating': review.rating,
            'review_date': review.review_date,
            'verified_purchase': review.verified_purchase,
        })
    return JsonResponse({'reviews': reviews_data})
