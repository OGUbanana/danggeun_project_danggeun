
from django.utils import timezone 
from .models import Product, ActivityArea, UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import CustomAuthForm, CustomUserForm, PostForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone as tz
from django.db.models import Q


def main(request):
    return render(request, 'main.html')

def search(request):
    return render(request, 'search.html')

def chat(request):
    return render(request, 'chat.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('market:main')
    else:
        form = CustomAuthForm(data=request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                user_id = form.cleaned_data['username']
                user_pwd = form.cleaned_data['password']
                user = authenticate(request, username=user_id, password=user_pwd)
                if user is not None:
                    login(request, user)
                    return redirect('market:main')
        return render(request, 'registration/login.html', {"form": form})

def user_logout(request):
    logout(request)
    return render(request, 'main.html')

def register(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            error_message = "이미 존재하는 아이디입니다."
        elif form.is_valid():
            
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            
            
            if password1 == password2:
                
                user = User.objects.create_user(username=username, password=password1)
                
                
                login(request, user)
            
            
                return redirect('market:login')
            else:
                form.add_error('password2', '비밀번호가 일치하지 않습니다')
    else:
        form = CustomUserForm()
    
    return render(request, 'registration/register.html', {'form': form, 'error_message': error_message})

def trade(request):
    products = Product.objects.filter(status='N').order_by('-refreshed_at', '-created_at')

    context = {
        'products' : products
    }
    
    return render(request, 'trade.html', context)

def location(request):
    return render(request, 'location.html')

def trade_post(request,product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.user.is_authenticated:
        if request.user != product.user:
            product.view_count += 1
            product.save()
    else:
        product.view_count += 1
        product.save()

    try:
        user_profile = UserProfile.objects.get(user=product.user)
    except UserProfile.DoesNotExist:
            user_profile = None

    context = {
        'product': product,
        'user_profile': user_profile,
    }
    return render(request, 'trade_post.html',context)


def alert(request, alert_message):
    return render(request, 'alert.html', {'alert_message': alert_message})


@login_required
def write(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        
        if user_profile.is_authenticated == 'Y':
            return render(request, 'write.html')
        else:
            return redirect('market:alert', alert_message='동네인증을 해주세요!!')
    except UserProfile.DoesNotExist:
        return redirect('market:alert', alert_message='동네인증을 해주세요!!')


def edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if product:
        product.description = product.description.strip()

    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'edit':
            product.title = request.POST['title']
            product.sell_price = request.POST['sell_price']
            product.description = request.POST['description']
            product.location = request.POST['location']
            if 'product_image' in request.FILES:
                product.product_image = request.FILES['product_image']
            product.save()
            return redirect('market:trade_post', product_id=product.pk)
        elif action == 'delete':
            product.delete()
            return redirect('market:trade')

    return render(request, 'write.html', {'product': product})

@login_required
def create_form(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('market:trade_post', product_id=product.pk)
        if not form.is_valid():
            print(form.errors)

    else:
        form = PostForm()
    return render(request, 'trade_post.html', {'form': form})


@login_required
def set_region(request):
    if request.method == 'POST':
        region = request.POST.get('region-setting')
        context = {
            'region': region,
        }
        if region:
            user = request.user
            try:
                activity_area = ActivityArea.objects.get(user_id=user)
            except ActivityArea.DoesNotExist:
                activity_area = ActivityArea(user_id=user)
            
            activity_area.emd_area_name = region
            activity_area.authenticated_at = timezone.now()
            activity_area.save()
        return render(request, 'location.html', context)
    return render(request, 'location.html')

def set_region_certification(request):
    return render(request, 'main.html')

# 끌어올리기
def pull_up(request, product_id) :
    username = request.user.username
    product = get_object_or_404(Product, pk=product_id)
    user_info = get_object_or_404(User, username=username)
    user_id = user_info.id

    if(product.user_id == user_id) :
        product.refreshed_at = tz.now();
        product.save()

        return redirect('market:trade')

def search(request):
    query = request.GET.get('search')
    if query:
        results = Product.objects.filter(Q(title__icontains=query) | Q(location__icontains=query))
    else:
        results = Product.objects.all()
    return render(request, 'search.html', {'products': results})
