from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Wishlist API')

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'wishes', views.WishViewSet, basename='wish')

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
