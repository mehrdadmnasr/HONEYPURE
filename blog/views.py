from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages

# Create your views here.
def blog(request):
    blogs = Blog.objects.order_by('-publish_date')

    data = {
        'blogs': blogs,
    }
    return render(request, 'blog/blog.html', data)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Blog

def blog_detail(request, id):
    try:
        single_blog = Blog.objects.get(pk=id)
    except Blog.DoesNotExist:
        messages.error(request, "این بلاگ وجود ندارد.")
        return redirect('blog')  # یا به صفحه دلخواه دیگر هدایت کنید

    tags = single_blog.tags
    num_tags = len(tags)

    row_width = 1000  # عرض کل سطر به پیکسل
    sample_tag_width = 100  # یک مقدار داینامیک از عرض هر تگ

    if sample_tag_width == 0:
        sample_tag_width = 100  # مقدار پیش‌فرض در صورت صفر بودن

    tags_per_row = row_width // sample_tag_width
    last_row_count = num_tags % tags_per_row

    if tags_per_row == 0:
        tags_per_row = 1  # مقدار پیش‌فرض در صورت صفر بودن

    if last_row_count == 0:
        last_row_count = tags_per_row

    empty_tags = tags_per_row - last_row_count

    data = {
        'single_blog': single_blog,
        'tags': tags,
        'empty_tags': range(empty_tags),
    }
    return render(request, 'blog/blog_detail.html', data)
