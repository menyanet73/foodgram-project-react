from django.urls import include, path, re_path
from rest_framework import routers
from users import views
from djoser.urls import authtoken
from djoser.views import TokenCreateView


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    path('users/', views.UsersView.as_view(), name='signup'),
    path('auth/', include('djoser.urls.authtoken')),
]