from django.urls import path
from . import views
from .forms import CustomUserForm, CustomAuthForm
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'market'

urlpatterns = [
    path('', views.main, name="main"),
    path('search/', views.search, name='search'),
    path('login/', views.user_login, name='login'),
     path('logout/', views.user_logout, name='logout'),
    path('chat/', views.chat, name='chat'),
    path('trade/', views.trade, name='trade'),
    path('register/', views.register, name='register'),
    path('location/', views.location, name='location'),
    path('trade_post/<int:product_id>', views.trade_post, name='trade_post'),
    path('set_region/', views.set_region, name='set_region'),
    path('set_region_certification/', views.set_region_certification, name='set_region_certification'),
    path('write/', views.write, name='write'),
    path('edit/<int:product_id>/', views.edit, name='edit'),
    path('create_form/', views.create_form, name='create_form'),

    path('alert/<str:alert_message>/', views.alert, name='alert'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
