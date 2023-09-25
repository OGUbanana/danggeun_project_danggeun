from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        label='아이디',
        widget=forms.TextInput(
            attrs={
                'placeholder': '아이디를 입력해주세요',
                'autofocus': True,
                'class': 'login-input',
            }
        )
    )
    password = forms.CharField(
        label='비밀번호',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호를 입력해주세요',
                'class': 'login-input',
            }
        )
    )
     # 콜론을 제거하려면 다음과 같이 라벨 속성을 공백으로 설정합니다.
    username.label = ""
    password.label = ""

    error_messages = {
        'invalid_login': '잘못된 아이디 또는 비밀번호입니다. 대소문자를 확인하여 주세요.',
        'inactive': '이 계정은 비활성화되었습니다. 관리자에게 문의하세요.',
    }

class CustomUserForm(UserCreationForm):
    username = forms.CharField(
        label='아이디',
        widget=forms.TextInput(
            attrs={
                'placeholder': '아이디를 입력해주세요',
                'autofocus': True,
                'class': 'login-input',
            }
        )
    )
    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호를 입력해주세요',
                'class': 'login-input',
            }
        )
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호를 다시 입력해주세요',
                'class': 'login-input',
            }
        )
    )
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class PostForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'product_image','location','sell_price', 'description']