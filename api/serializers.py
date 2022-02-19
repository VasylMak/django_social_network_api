from django.contrib.auth.models import User
from rest_framework import serializers
from posts.models import LikeDate, Post


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source='likes.count', read_only=True)
    dislikes = serializers.IntegerField(source='dislikes.count',read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        fields = '__all__'


class PostAnaliticsLikesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LikeDate
        fields = '__all__'


class UserAnaliticsActivitySerializer(serializers.ModelSerializer):
    last_request = serializers.CharField(source='profile.last_request')
    
    class Meta:
        model = User
        fields = ['username', 'date_joined', 'last_request']


class AddLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['likes']


class AddDislikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['dislikes']