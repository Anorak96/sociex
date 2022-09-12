from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('<pk>/', views.UserDetailView.as_view(), name='profile'),
    path('follow/<pk>', views.FollowView.as_view(), name='follow'),
    path('<pk>/update/', views.UserUpdateView.as_view(), name='update'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
]