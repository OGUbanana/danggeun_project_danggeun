from django.shortcuts import render

def main(request):
    return render(request, 'main.html')

def search(request):
    return render(request, 'search.html')

def chat(request):
    return render(request, 'chat.html')

def login(request):
    return render(request, 'registration/login.html')

# def logout(request):
#     return render(request, 'registration/logout.html')
def register(request):
    return render(request, 'registration/register.html')

def trade(request):
    return render(request, 'trade.html')

def location(request):
    return render(request, 'location.html')

def trade_post(request):
    return render(request, 'trade_post.html')

def write(request):
    return render(request, 'write.html')
