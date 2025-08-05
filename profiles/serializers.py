# profiles/serializers.py

from rest_framework import serializers
from .models import Profile, Link
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'title', 'url', 'click_count']

class ProfileSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'name', 'bio', 'slug', 
            'profile_image', 'theme', 'links'
        ]

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user