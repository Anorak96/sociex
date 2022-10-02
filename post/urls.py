from django.urls import path
from post.views import views
from post.views import jsonview

app_name = 'post'
urlpatterns = [
    path('', views.PostListView.as_view(), name='posts'),
    path('post/<pk>/', views.PostDetailView.as_view(), name='detail'),
    # path('like/', views.LikeView.as_view(), name='like_post'),
    path('create/', views.PostCreate.as_view(), name='create_post'),
    path('create_comment/', views.CommentCreate.as_view(), name='create_comment'),
    path('post/<pk>/delete/', views.PostDeleteView.as_view(), name='delete'),
    path('post/<pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('comment/<pk>/delete/', views.CommentDeleteView.as_view(), name='comm_delete'),
    path('comment/<pk>/update/', views.CommentUpdateView.as_view(), name='comm_update'),
    path('spin', views.Post_json.as_view(), name='post_spin'),
    
    #=========================JSON=====================================
    
    path('comment/<pk>', jsonview.CommentJson.as_view(), name='comment_json'),
    path('post_json', jsonview.post_json, name='post_json'),
    path('post/<pk>/like/', jsonview.LikeView.as_view(), name='like_post'),
]