
from django.utils import timezone 
from .models import Product, ActivityArea, UserProfile, WishList, ChatRoom, ChatMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import CustomAuthForm, CustomUserForm, PostForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone as tz
from django.db.models import Q
from django.http import HttpResponseNotAllowed
from django.utils.decorators import method_decorator
import openai
from django.http import JsonResponse
from django.views import View


def main(request):
    return render(request, 'main.html')


def search(request):
    return render(request, 'search.html')

@login_required
def chat_view(request):
    return render(request, 'chat.html')

# 채팅 ################################################################################

# 채팅테스트

def index(request): 
    return render(request, 'chat_index.html')


# 채팅방 열기
def chat_room(request, pk):
    user = request.user
    chat_room = get_object_or_404(ChatRoom, pk=pk)

    # 내 ID가 포함된 방만 가져오기
    chat_rooms = ChatRoom.objects.filter(
            Q(receiver_id=user) | Q(starter_id=user)
        ).order_by('-latest_message_time')  # 최신 메시지 시간을 기준으로 내림차순 정렬
    
    # 각 채팅방의 최신 메시지를 가져오기
    chat_room_data = []
    for room in chat_rooms:
        latest_message = ChatMessage.objects.filter(chatroom=room).order_by('-timestamp').first()
        if latest_message:
            chat_room_data.append({
                'chat_room': room,
                'latest_message': latest_message.content,
                'timestamp': latest_message.timestamp,
            })

    # 상대방 정보 가져오기
    if chat_room.receiver == user:
        opponent = chat_room.starter
    else:
        opponent = chat_room.receiver

    opponent_user = User.objects.get(pk=opponent.pk)


    # post의 상태 확인 및 처리
    if chat_room.product is None:
        seller = None
        product = None
    else:
        seller = chat_room.product.user
        product = chat_room.product

    return render(request, 'chat_room.html', {
        'chat_room': chat_room,
        'chat_room_data': chat_room_data,
        'room_name': chat_room.pk,
        'seller': seller,
        'product': product,
        'opponent': opponent_user,
    })


# 채팅방 생성 또는 참여
def create_or_join_chat(request, pk):
    product = get_object_or_404(Product, pk=pk)
    user = request.user
    chat_room = None
    created = False

    # 채팅방이 이미 존재하는지 확인
    chat_rooms = ChatRoom.objects.filter(
        Q(starter=user, receiver=product.user, product=product) |
        Q(starter=product.user, receiver=user, product=product)
    )
    if chat_rooms.exists():
        chat_room = chat_rooms.first()
    else:
        # 채팅방이 존재하지 않는 경우, 새로운 채팅방 생성
        chat_room = ChatRoom(starter=user, receiver=product.user, product=product)
        chat_room.save()
        created = True

    return JsonResponse({'success': True, 'chat_room_id': chat_room.pk, 'created': created})


# 가장 최근 채팅방 가져오기
@login_required
def get_latest_chat(request, pk):
    user = request.user
    # 1) 해당 pk인 채팅방 중 가장 최신 채팅방으로 리디렉션
    try:
        latest_chat_with_pk = ChatRoom.objects.filter(
            Q(product_id=pk) &
            (Q(receiver=user) | Q(starter=user))
        ).latest('latest_message_time')
        return JsonResponse({'success': True, 'chat_room_id': latest_chat_with_pk.room_number})
    except ChatRoom.DoesNotExist:
        pass

    # 2) 위 경우가 없다면 내가 소속된 채팅방 전체 중 가장 최신 채팅방으로 리디렉션
    try:
        latest_chat = ChatRoom.objects.filter(
            Q(receiver=user) | Q(starter=user)
        ).latest('latest_message_time')
        return JsonResponse({'success': True, 'chat_room_id': latest_chat.room_number})

    # 3) 모두 없다면 현재 페이지로 리디렉션
    except ChatRoom.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'alert_message': '진행중인 채팅이 없습니다.'
        })

        
# nav/footer에서 채팅하기 눌렀을 때
@login_required
def get_latest_chat_no_pk(request):
    user = request.user
    try:
        latest_chat = ChatRoom.objects.filter(
            Q(receiver=user) | Q(starter=user),
            latest_message_time__isnull=False
        ).latest('latest_message_time')
        return redirect('market:chat_room', pk=latest_chat.room_number)

    except ChatRoom.DoesNotExist:
        return redirect('market:alert', alert_message='진행중인 채팅이 없습니다.', redirect_url='current')
    
@method_decorator(login_required, name='dispatch')
class ConfirmDealView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        user = request.user

        previous_url = request.META.get('HTTP_REFERER')
        url_parts = previous_url.split('/')
        original_product_id = url_parts[-2] if url_parts[-1] == '' else url_parts[-1]

        chat_room = get_object_or_404(ChatRoom, room_number=original_product_id)


        if chat_room.starter == user:
            other_user = chat_room.receiver
        else:
            other_user = chat_room.starter

        if chat_room is None:
            messages.error(request, 'Chat room does not exist.')
            return redirect('market:trade')
        
        # buyer를 설정하고, product_sold를 Y로 설정
        product.buyer = chat_room.receiver if chat_room.starter == product.user else chat_room.starter
        product.status = 'Y'
        product.save()
        
        # 거래가 확정되면 새로고침
        return redirect('market:chat_room', pk=chat_room.room_number)

# 채팅 끝 ################################################################################



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
                form.add_error('password2', '비밀번호가 일치하지 않습니다')
    else:
        form = CustomUserForm()
    
    return render(request, 'registration/register.html', {'form': form, 'error_message': error_message})

def trade(request):
    products = Product.objects.filter(Q(status='N') | Q(status='R')).order_by('-refreshed_at', '-created_at')

    context = {
        'products' : products
    }
    
    return render(request, 'trade.html', context)

def location(request):
    return render(request, 'location.html')

def trade_post(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.user.is_authenticated:
        if request.user != product.user:
            product.view_count += 1
            product.save()
    else:
        product.view_count += 1
        product.save()

    chatrooms = ChatRoom.objects.filter(product=product)
    try:
        user_profile = UserProfile.objects.get(user=product.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    wishlist = None
    if request.user.is_authenticated:
        try:
            wishlist = WishList.objects.get(product_id=product_id, user_id=request.user.id)
        except WishList.DoesNotExist:
            pass

    context = {
        'product': product,
        'user_profile': user_profile,
        'wishlist': wishlist,
        'chatrooms': chatrooms
    }

    return render(request, 'trade_post.html', context)

# 상품 상태 업데이트
def product_status(request, product_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    product = get_object_or_404(Product, pk=product_id)

    new_status = request.POST.get('status')
    selected_chatroom_id = request.POST.get('selected_chatroom', None)

    if new_status == 'R' and selected_chatroom_id:
        chatroom = get_object_or_404(ChatRoom, pk=selected_chatroom_id)
        if chatroom.product == product:
            product.status = 'R'
            product.save()

    elif new_status == 'Y' and selected_chatroom_id:
        chatroom = get_object_or_404(ChatRoom, pk=selected_chatroom_id)
        if chatroom.product == product:
            product.status = 'Y'
            product.buyer = chatroom.receiver
            product.save()

    elif new_status == 'N':
        product.status = 'N'
        product.save()

    return redirect('market:trade_post', product_id=product.pk)




def alert(request, alert_message):
    return render(request, 'alert.html', {'alert_message': alert_message})


@login_required
def write(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        
        if user_profile.is_authenticated == 'Y':
            return render(request, 'write.html')
        else:
            return redirect('market:alert', alert_message='동네인증을 해주세요!!')
    except UserProfile.DoesNotExist:
        return redirect('market:alert', alert_message='동네인증을 해주세요!!')


def edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if product:
        product.description = product.description.strip()

    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'edit':
            product.title = request.POST['title']
            product.sell_price = request.POST['sell_price']
            product.description = request.POST['description']
            product.location = request.POST['location']
            if 'product_image' in request.FILES:
                product.product_image = request.FILES['product_image']
            product.save()
            return redirect('market:trade_post', product_id=product.pk)
        elif action == 'delete':
            product.delete()
            return redirect('market:trade')

    return render(request, 'write.html', {'product': product})

@login_required
def create_form(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('market:trade_post', product_id=product.pk)
        if not form.is_valid():
            print(form.errors)

    else:
        form = PostForm()
    return render(request, 'trade_post.html', {'form': form})


@login_required
def set_region(request):
    if request.method == 'POST':
        region = request.POST.get('region-setting')
        context = {
            'region': region,
        }
        if region:
            user = request.user
            try:
                activity_area = ActivityArea.objects.get(user_id=user)
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.region = region
                user_profile.save()
            except ActivityArea.DoesNotExist:
                activity_area = ActivityArea(user_id=user)
            
            activity_area.emd_area_name = region
            activity_area.authenticated_at = timezone.now()
            activity_area.save()
        return render(request, 'location.html', context)
    return render(request, 'location.html')

@login_required
def set_region_certification(request):
    if request.method == 'POST':
        user = request.user
        try:
            userprofile = UserProfile.objects.get(user=user)
            userprofile.is_authenticated = 'Y'
            userprofile.save()
        except UserProfile.DoesNotExist:
            userprofile = UserProfile(user=user, is_authenticated='Y')
            userprofile.save()
    return render(request, 'main.html')


# 끌어올리기
def pull_up(request, product_id) :
    username = request.user.username
    product = get_object_or_404(Product, pk=product_id)
    user_info = get_object_or_404(User, username=username)
    user_id = user_info.id

    if(product.user_id == user_id) :
        product.refreshed_at = tz.now();
        product.save()

        return redirect('market:trade')
    
# 찜하기
def add_dibs(request, product_id):

    user = request.user
    username = request.user.username
    user_info = get_object_or_404(User, username=username)
    user_id = user_info.id
    product = get_object_or_404(Product, product_id=product_id)
    
    try:
        wishlist_item = WishList.objects.get(user_id_id=user_id, product_id=product_id)
        wishlist_item.delete()

        return redirect('market:trade_post', product_id=product.pk)

    except WishList.DoesNotExist:
        
        wishlist = WishList(user_id=user)
        wishlist.product_id = product_id
        wishlist.created_at = tz.now()
        wishlist.save()

        return redirect('market:trade_post', product_id=product.pk)

def search(request):
    query = request.GET.get('search')
    if query:
        results = Product.objects.filter(Q(title__icontains=query) | Q(location__icontains=query))
    else:
        results = Product.objects.all()
    return render(request, 'search.html', {'products': results})


@login_required
def mypage(request):
    return render(request, 'mypage.html')

@login_required
def sell_list(request):
    products = Product.objects.filter(user=request.user).order_by('-refreshed_at', '-created_at')


    context = {
        'products' : products
    }
    
    return render(request, 'sell_list.html', context)

@login_required
def buy_list(request):

    products = Product.objects.filter(buyer=request.user).order_by('-refreshed_at', '-created_at')

    context = {
        'products' : products
    }
    return render(request, 'sell_list.html', context)

@login_required
def wish_list(request):
    username = request.user.username
    user = get_object_or_404(User, username=username)
    user_id = user.id
    wish_list = WishList.objects.filter(user_id=user_id).order_by('-created_at')
    wish_product = []

    for item in wish_list :
        product = Product.objects.get(product_id=item.product_id)
        wish_product.append(product)

    context = {
        'wish_product' : wish_product,
    }
    
    return render(request, 'my_list.html', context)



def chatbot(request):
    openai.api_key = settings.OPENAI_API_KEY
    user_input = request.GET.get('message', '')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 당근 마켓이라는 중고 거래 사이트에서 도움을 주는 비서입니다."},
            {"role": "user", "content": f"'{user_input}'에 대한 답변을 적어주세요. 50자 이내로 작성해주세요."}
        ]
    )
    bot_response = response.choices[0].message['content'].strip()

    # '!'로 시작하는 키워드를 포함하고 있으면 추천 알고리즘 실행
    if user_input.startswith('!'):
        keyword = user_input[1:].strip()
        recommended_products = recommend_products(keyword)
        
        if not recommended_products:
            return JsonResponse({
                "type": "text",
                "data": f"'{keyword}'에 해당하는 상품이 없습니다."
            })
        else:
            return JsonResponse({
                "type": "product_recommendation",
                "data": {
                    "message": f"다음은 '{keyword}' 관련 추천 상품입니다:",
                    "products": recommended_products
                }
            })

    return JsonResponse({"type": "text", "data": bot_response})



def recommend_products(keyword, limit=5):
    products = Product.objects.filter(title__icontains=keyword).order_by('-product_id')[:limit] 
    product_data = [{
        'product_id': product.product_id,
        'title': product.title,
        'price': f"{product.sell_price}원",
        'image_url': product.product_image.url if product.product_image else None
    } for product in products]
    return product_data


def chat_page(request):
    user = request.user

    # 내 ID가 포함된 방만 가져오기
    chat_rooms = ChatRoom.objects.filter(
            Q(receiver_id=user) | Q(starter_id=user)
        ).order_by('-latest_message_time')  # 최신 메시지 시간을 기준으로 내림차순 정렬
    
    # 각 채팅방의 최신 메시지를 가져오기
    chat_room_data = []
    for room in chat_rooms:
        latest_message = ChatMessage.objects.filter(chatroom=room).order_by('-timestamp').first()
        if latest_message:
            chat_room_data.append({
                'chat_room': room,
                'latest_message': latest_message.content,
                'timestamp': latest_message.timestamp,
            })

    return render(request, 'chatbot.html', {
        'chat_room_data': chat_room_data,
    })