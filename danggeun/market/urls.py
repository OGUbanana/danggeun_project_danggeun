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
    path('product_status/<int:product_id>', views.product_status, name='product_status'),
    path('trade_post/<int:product_id>/<str:user_error>/', views.trade_post, name='trade_post_with_error'),
    path('set_region/', views.set_region, name='set_region'),
    path('set_region_certification/', views.set_region_certification, name='set_region_certification'),
    path('write/', views.write, name='write'),
    path('edit/<int:product_id>/', views.edit, name='edit'),
    path('create_form/', views.create_form, name='create_form'),

    path('alert/<str:alert_message>/', views.alert, name='alert'),
    
    # 끌어올리기
    path('pull_up/<int:product_id>', views.pull_up, name='pull_up'),
    # 찜하기
    path('dibs/<int:product_id>', views.add_dibs, name='dibs'),

    path('mypage/',views.mypage, name='mypage'),
    path('sell_list/', views.sell_list, name='sell_list'),
    path('buy_list/', views.buy_list, name='buy_list'),
    path('wish_list/', views.wish_list, name='wish_list'),
    path('chatai/', views.chatbot, name='chatai'),
    path('chatbot/', views.chat_page, name='chatbot')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

