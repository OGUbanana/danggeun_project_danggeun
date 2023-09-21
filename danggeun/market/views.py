from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .models import Product, ActivityArea
from .forms import CustomUserForm

def main(request):
    return render(request, 'main.html')

def search(request):
    return render(request, 'search.html')

def chat(request):
    return render(request, 'chat.html')

# def login(request):
#     form = CustomAuthForm(data=request.POST or None)
#     if request.method == "POST":
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('market:index')
#     return render(request, 'registration/login.html', {'form': form})


# def logout(request):
#     return render(request, 'registration/logout.html')
def signup(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('market:main')
    else:
        form = CustomUserForm()
    return render(request, 'registration/register.html', {'form': form})

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

def write(request):
    return render(request, 'write.html')
