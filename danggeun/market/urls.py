from django.urls import path
from . import views

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
    path('trade_post/', views.trade_post, name='trade_post'),
    path('write/', views.write, name='write'),

]