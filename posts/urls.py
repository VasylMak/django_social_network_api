from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('users', views.UserListView.as_view(), name='user_list'),
    path('registration/register', views.user_register, name='user_register'),
    path('post/create/', views.PostCreate.as_view(), name='post_create'),
    path('post/<int:pk>/like', views.AddLike.as_view(), name='like'),
    path('post/<int:pk>/dislike', views.AddDislike.as_view(), name='dislike'),
]