from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, WishSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WishViewSet(viewsets.ModelViewSet):
    serializer_class = WishSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self, *args, **kwargs):
        return self.request.user.wishes.all()
