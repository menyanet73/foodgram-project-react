from django.urls import include, path
from rest_framework import routers

from users import views


router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
