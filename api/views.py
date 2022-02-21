from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import (
    ListCreateAPIView,
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
)

from posts.models import Post, LikeDate

from .serializers import (
    PostSerializer,
    UserSerializer,
    PostAnaliticsLikesSerializer,
    UserAnaliticsActivitySerializer,
    AddLikeSerializer,
    AddDislikeSerializer,
)


# GET and POST posts by API
class PostAPI(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['creator'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "status": True,
                "message": "Post created!",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED, headers=headers
        )


# PUT likes by API
class AddLikeAPI(UpdateAPIView):
    serializer_class = AddLikeSerializer
    post_id = 'pk'

    def get_queryset(self):
        url_post_id = self.kwargs.get(self.post_id)
        filtered_queryset = Post.objects.filter(id=url_post_id)
        return filtered_queryset
    
    def update(self, request, *args, **kwargs):
        like_field = self.get_object().likes
        dislike_object = self.get_object()
        dislike_field = AddDislikeSerializer(dislike_object).data['dislikes']
        user_id = request.user.id
        if user_id not in list(dislike_field):
            like_field.add(user_id)
            return Response(
                {
                    "status": True,
                    "message": "Like added!",
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "status": False,
                    "message": "Like can't be added to disliked posts.",
                },
                status=status.HTTP_400_BAD_REQUEST
            )


# PUT dislikes by API
class AddDislikeAPI(UpdateAPIView):
    serializer_class = AddDislikeSerializer
    post_id = 'pk'

    def get_queryset(self):
        url_post_id = self.kwargs.get(self.post_id)
        filtered_queryset = Post.objects.filter(id=url_post_id)
        return filtered_queryset
    
    def update(self, request, *args, **kwargs):
        dislike_field = self.get_object().dislikes
        like_object = self.get_object()
        like_field = AddLikeSerializer(like_object).data['likes']
        user_id = request.user.id
        if user_id not in list(like_field):
            dislike_field.add(user_id)
            return Response(
                {
                    "status": True,
                    "message": "Dislike added!",
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "status": False,
                    "message": "Dislike can't be added to liked posts.",
                },
                status=status.HTTP_400_BAD_REQUEST
            )


# POST users by API
class UserAPI(CreateAPIView):
    model = get_user_model()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class PostAnaliticsLikesAPI(ListAPIView):
    serializer_class = PostAnaliticsLikesSerializer
    date_from = 'date_from'
    date_to = 'date_to'

    def get_queryset(self):
        url_date_from = self.kwargs.get(self.date_from)
        url_date_to = self.kwargs.get(self.date_to)
        filtered_queryset = LikeDate.objects.filter(
            created__range=[url_date_from, url_date_to]
        )
        return filtered_queryset


# GET users activity by API
class UserAnaliticsActivityAPI(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserAnaliticsActivitySerializer
    permission_classes = (IsAuthenticated,)