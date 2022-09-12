from django.db import models
import os
from django.core.validators import FileExtensionValidator
from uuid import uuid4
from user.models import User
from django.db.models import Max

def get_message_image(instance, filename):
    upload_to = '{}/{}/{}_{}'.format('message', instance.chat.sender_user, 'to', instance.chat.receiver_user)
    ext = filename.split('.')[-1]
    filename = '{}_{}_{}_{}.{}'.format(instance.chat.sender_user, 'to', instance.chat.receiver_user, uuid4().hex, ext)
    return os.path.join(upload_to, filename)

class Chat(models.Model):
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sender')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_receiver')
    body = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def get_messages(user):
        chats = Chat.objects.filter(sender_user=user).values('receiver_user').annotate(last=Max('date')).order_by('-last')
        users = []
        for chat in chats:
            users.append({
                'receiver_user': User.objects.get(pk=chat['receiver_user']),
                'last': chat['last'],
                'unread': Chat.objects.filter(sender_user=chat['receiver_user'], receiver_user__pk=user, read=False).count(),
                })
        return users

class Image(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_images')
    image = models.ImageField(upload_to=get_message_image, blank=True, null=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
