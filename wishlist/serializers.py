from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Wish


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class WishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ('id', 'title', 'price', 'link', 'description')
