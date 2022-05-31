from django.urls import include, path, re_path
from rest_framework import routers
from users import views
from djoser.urls import authtoken
from djoser.views import TokenCreateView


# router = routers.DefaultRouter()
router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet, basename='users')
# router.register(
#     r'users/(?P<user_id>\d+)',
#     views.FollowViewset,
#     basename='subscribe')


urlpatterns = [
    # path('users/', views.UsersView.as_view(), name='signup'),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]