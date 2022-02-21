from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.urls import path
from . import views


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('post/', views.PostAPI.as_view(), name='post_api'),
    path('post/<int:pk>/like', views.AddLikeAPI.as_view(), name='like_api'),
    path(
        'post/<int:pk>/dislike',
        views.AddDislikeAPI.as_view(),
        name='like_api'
    ),
    path(
        'post/analitics/date_from=<date_from>&date_to=<date_to>/',
        views.PostAnaliticsLikesAPI.as_view(),
        name='post_analitics'
    ),
    path('user/', views.UserAPI.as_view(), name='user_api'),
    path(
        'user/analitics/',
        views.UserAnaliticsActivityAPI.as_view(),
        name='user_analitics'
    ),
]