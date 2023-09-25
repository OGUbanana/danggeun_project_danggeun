
from .models import Product, ActivityArea, UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import CustomAuthForm, CustomUserForm, PostForm
from django.contrib.auth.models import User

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
                form.add_error('password2', 'Passwords do not match')
    else:
        form = CustomUserForm()
    
    return render(request, 'registration/register.html', {'form': form, 'error_message': error_message})

def trade(request):
    products = Product.objects.all().order_by('-created_at')

    for product in products:
        product.activity_area = ActivityArea.objects.get(user_id=product.user_id)

    context = {
        'products' : products
    }
    
    return render(request, 'trade.html', context)

def location(request):
    return render(request, 'location.html')

def trade_post(request,product_id):
    products = Product.objects.get(pk=product_id)
    return render(request, 'trade_post.html')


def alert(request, alert_message):
    return render(request, 'alert.html', {'alert_message': alert_message})

# 거래글쓰기 화면
@login_required
def write(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        
        if user_profile.is_authenticated == 'Y':
            return render(request, 'write.html')
        else:
            return redirect('market:alert', alert_message='동네인증이 필요합니다.')
    except UserProfile.DoesNotExist:
        return redirect('market:alert', alert_message='동네인증이 필요합니다.')

# 거래글수정 화면
def edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product:
        product.description = product.description.strip()
    if request.method == "POST":
        product.title = request.POST['title']
        product.price = request.POST['price']
        product.description = request.POST['description']
        product.activity_area = ActivityArea.objects.get(user_id=product.user_id)
        product.activity_area = request.POST['location']
        if 'images' in request.FILES:
            product.images = request.FILES['images']
        product.save()
        return redirect('market:trade_post', pk=product_id)

    return render(request, 'write.html', {'product': product})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user_id = request.user.id  # 작성자 정보 추가
            product.save()  # 최종 저장
            return redirect('marekt:trade_post', pk=product.pk)  # 저장 후 상세 페이지로 이동
    else:
        form = PostForm()
    return render(request, 'trade_post.html', {'form': form})


def set_region(request):
    if request.method == 'POST':
        region = request.POST.get('region-setting')
        context = {
            'region': region,
        }
        return render(request, 'location.html', context)
    return render(request, 'location.html')