from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
#from contacts.models import Contact
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            next_url = request.POST.get('next')  # دریافت مقدار next
            if not next_url:  # اگر مقدار next وجود ندارد
                next_url = 'dashboard'  # هدایت به داشبورد به عنوان مقدار پیش‌فرض
            messages.success(request, 'You are now logged in.')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    # بررسی اگر پیغام از `checkout` آمده است
    if 'next' in request.GET and 'checkout' in request.GET.get('next'):
        messages.info(request, 'Please log in to proceed with checkout.')


    return render(request, 'accounts/login.html', {'next': request.GET.get('next', '')})

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists!')
                return redirect('register')
            else:
                #user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
                #auth.login(request, user)
                #messages.success(request, 'You are now logged in.')
                #return redirect('dashboard')
                #user.  save()
                #messages.success(request, 'You are registered successfully.')
                #return redirect('login')
                user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
                user.save()
                auth.login(request, user)
                messages.success(request, 'You are now logged in.')
                return redirect('dashboard')
        else:
            messages.error(request, 'password do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

@login_required(login_url='login')
def dashboard(request):
#    user_inquiry = Contact.objects.order_by('-create_date').filter(user_id=request.user.id)
    data = {
#        'inquiries':user_inquiry,
    }
    return render(request, 'accounts/dashboard.html', data)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are successfully logged out.')
        return redirect('home')
    return redirect('home')
