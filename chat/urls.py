from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    path('', views.ChatView.as_view(), name='chat_index'),
    path('<pk>', views.ChatDirectView.as_view(), name='chat_direct'),
    path('send/<pk>/', views.SendChat.as_view(), name='send_chat'),
    path('receive/<pk>/', views.ReceiveChat.as_view(), name='receive_chat'),
    path('notification/', views.ChatNotif.as_view(), name='notif_chat'),
]