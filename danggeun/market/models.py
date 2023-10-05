from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    region = models.CharField(max_length=100, null=True)
    is_authenticated = models.CharField(max_length=1, default='N')

    def __str__(self):
        return f'{self.user.username} Profile'

# 상품
class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, db_index=True)
    status = models.CharField(max_length=10, default='N')
    product_image = models.ImageField(upload_to='product_images/')  
    location = models.CharField(max_length=100)
    sell_price = models.IntegerField(null=True)
    view_count = models.IntegerField(default=0)
    description = models.TextField()
    refreshed_at = models.DateTimeField(db_index=True, auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    buyer = models.ForeignKey(User, related_name='purchased_posts', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'product'

# 관심상품        
class WishList(models.Model):
    like_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.BigIntegerField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'wish_lists'
        
# 채팅방
class ChatRoom(models.Model):
    room_number = models.AutoField(primary_key=True)
    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='started_chats')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    latest_message_time = models.DateTimeField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='chat_rooms', null=True, blank=True)


    def __str__(self):
        return f'ChatRoom: {self.starter.username} and {self.receiver.username}'



# 채팅 메시지        
class ChatMessage(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message: {self.author.username} at {self.timestamp}'

    class Meta:
        ordering = ['timestamp']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 새 메시지가 저장될 때마다 chatroom의 latest_message_time을 업데이트
        self.chatroom.latest_message_time = self.timestamp
        self.chatroom.save()


# 활동지역
class ActivityArea(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # distance_meters = models.SmallIntegerField()
    emd_area_name = models.CharField(max_length=255, db_index=True)
    authenticated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'activity_areas'
        
