from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .forms import ChatForm
from django.db.models import Max
from django.views import generic
from django.db.models import Q
from user.models import User
from .models import Chat, Image
from django.contrib.auth.mixins import LoginRequiredMixin

class ChatView(LoginRequiredMixin, generic.View):
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'
    model = Chat
    template_name = "chat/chat.html"

    def get(self, request):
        form = ChatForm()
        user = request.user
        chats = Chat.get_messages(user=user)
        directs = None
        active_user = None

        if chats:
            chat = chats[0]
            active_user = chat['receiver_user']
            directs = Chat.objects.filter(sender_user=user, receiver_user=chat['receiver_user'])
            directs.update(read=True)

            for chat in chats:
                if chat['receiver_user'] == active_user:
                    chat['unread'] = 0
        context={
            'directs' : directs,
            'active_user' : active_user,
            'chats' : chats,
            'form' : form,            
        }
        return render(request, self.template_name, context)

class ChatDirectView(LoginRequiredMixin, generic.View):
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'
    model = Chat
    template_name = "chat/chat.html"

    def get(self, request, pk):
        form = ChatForm()
        user = request.user
        chats = Chat.get_messages(user=user)
        active_user = pk
        directs = Chat.objects.filter(Q(sender_user=user, receiver_user=pk) | Q(sender_user=pk, receiver_user=user)).annotate(last=Max('date')).order_by('last')
        directs.update(read=True)
        for chat in chats:
            if chat['receiver_user'].username == pk:
                chat['unread'] = 0

        context = {
            'user' : user,
            'form' : form,
            'directs' : directs,
            # 'chat_num' : chats.count(),
            'chats' : chats,
            'active_user' : active_user,
            'num' : directs.count(),
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = ChatForm(request.POST)
        sender_user = request.user
        receiver__user = request.POST.get('receiver_user')
        receiver_user = User.objects.get(pk=receiver__user)
        body = request.POST.get('body')
        
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.sender_user = sender_user
            chat_message.receiver_user = receiver_user
            chat_message.body = body
            chat_message.save()
            return redirect("chat:chat_direct", pk=receiver_user.pk)
        
        context={
            'form' : form,
        }
        return render(request, self.template_name, context)

class SendChat(LoginRequiredMixin, generic.View):
    model = Chat
    template_name = 'chat/chat.html'

    def post(self, request, pk):
        sender_user = request.user
        receiver_user = User.objects.get(pk=pk)
        data = json.loads(request.body)
        newchat = data["body"]
        newchatid = Chat.objects.create(body=newchat, sender_user=sender_user, receiver_user=receiver_user, read=False)
        print(newchat)
        return JsonResponse(newchatid.body, safe=False)

class ReceiveChat(LoginRequiredMixin, generic.View):
    model = Chat
    template_name = 'chat/chat.html'

    def get(self, request, pk):
        sender_user = request.user
        receiver_user = User.objects.get(pk=pk)
        arr = []
        newchatid = Chat.objects.filter(sender_user=receiver_user, receiver_user=sender_user)
        for chat in newchatid:
            arr.append(chat.body)
        return JsonResponse(arr, safe=False)

class ChatNotif(LoginRequiredMixin, generic.View):
    model = Chat
    template_name = 'chat/chat.html'

    def get(self, request):
        user = request.user
        chats = Chat.get_messages(user=user)
        arr = []
        for chat in chats:
            msg = Chat.objects.filter(sender_user=chat['receiver_user'], receiver_user=user, read=False)
            arr.append(msg.count())
        return JsonResponse(arr, safe=False)