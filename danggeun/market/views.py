from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import CustomAuthForm, CustomUserForm
from django.contrib.auth.models import User

def main(request):
    return render(request, 'main.html')

def search(request):
    return render(request, 'search.html')

def chat(request):
    return render(request, 'chat.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('main')
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
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()

            user_id = form.cleaned_data['username']
            user_pwd = form.cleaned_data['password']
            user = authenticate(request, username=user_id, password=user_pwd)
            login(request, user)
            return redirect('market:main')
    else:
        form = CustomUserForm()
    return render(request, 'registration/register.html', {"form": form})

def trade(request):
    return render(request, 'trade.html')

def location(request):
    return render(request, 'location.html')

def trade_post(request):
    return render(request, 'trade_post.html')

def write(request):
    return render(request, 'write.html')
