from django.urls import path
from . import views
from .forms import CustomUserForm, CustomAuthForm
from django.contrib.auth import views as auth_views

app_name = 'market'

urlpatterns = [
    path('', views.main, name="main"),
    path('search/', views.search, name='search'),
    path('login/', views.user_login, name='login'),
     path('logout/', views.user_logout, name='logout'),
    path('chat/', views.chat, name='chat'),
    path('trade/', views.trade, name='trade'),
    # path('register/', views.signup, name='register'),
    path('location/', views.location, name='location'),
    path('trade_post/<int:product_id>', views.trade_post, name='trade_post'),
    path('set_region/', views.set_region, name='set_region'),
    path('write/', views.write, name='write'),

]