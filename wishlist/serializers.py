from django.contrib.auth.models import User
from rest_framework import serializers, validators

from .models import Wish


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            validators.UniqueValidator(queryset=User.objects.all())
        ]
    )
    username = serializers.CharField(
        max_length=32,
        validators=[
            validators.UniqueValidator(queryset=User.objects.all())
        ]
    )
    password = serializers.CharField(
        min_length=8,
        write_only=True
    )
    auth_token = serializers.SlugRelatedField(
        read_only=True,
        slug_field='key',
    )

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'auth_token')


class WishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ('id', 'title', 'price', 'link', 'description')
