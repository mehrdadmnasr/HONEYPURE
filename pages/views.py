from django.shortcuts import render, get_object_or_404
from .models import Team
from products.models import Product
from blog.models import Blog

# Create your views here.
def home(request):
	teams = Team.objects.all()
	all_products = Product.objects.order_by('-created_date')
	blogs = Blog.objects.order_by('-publish_date')
	data = {
		'teams': teams,
        'all_products': all_products,
		'blogs': blogs,
	}
	return render(request, 'pages/home.html', data)

def about(request):
	teams = Team.objects.all()
	data = {
		'teams': teams,
	}
	return render(request, 'pages/about.html', data)

def contact(request):
	return render(request, 'pages/contact.html')

def team_detail(request, id):
    single_team = get_object_or_404(Team, pk=id)
    data = {
        'single_team': single_team,
    }
    return render(request, 'pages/team_detail.html', data)
