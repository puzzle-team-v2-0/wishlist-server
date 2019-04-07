from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer, WishSerializer
from .models import Wish


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WishViewSet(viewsets.ModelViewSet):
    queryset = Wish.objects.all()
    serializer_class = WishSerializer
