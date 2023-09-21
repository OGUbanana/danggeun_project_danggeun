from django.urls import path
from . import views
from .forms import CustomUserForm, CustomAuthForm
from django.contrib.auth import views as auth_views

app_name = 'market'

urlpatterns = [
    path('', views.main, name="main"),
    path('search/', views.search, name='search'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=CustomAuthForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('login/', views.login, name='login'),
    path('chat/', views.chat, name='chat'),
    path('trade/', views.trade, name='trade'),
    path('register/', views.signup, name='register'),
    path('location/', views.location, name='location'),
    path('trade_post/<int:product_id>', views.trade_post, name='trade_post'),
    path('set_region/', views.location, name='set_region'),
    path('write/', views.write, name='write'),

]