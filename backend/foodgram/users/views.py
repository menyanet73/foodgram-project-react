from django.shortcuts import get_object_or_404
from djoser import views
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from users import models, serializers


class UserViewSet(views.UserViewSet):

    def get_serializer_class(self):
        if self.action in ['subscribe', 'subscriptions']:
            return serializers.FollowSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        user = get_object_or_404(
            models.User, username=request.data['username'])
        return Response(
            {
                "email": user.email,
                "id": user.pk,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }, status=status.HTTP_200_OK
        )

    @action(['get'], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action(['post', 'delete'], detail=True)
    def subscribe(self, request, id, *args, **kwargs):
        follower = request.user
        following = get_object_or_404(models.User, id=id)
        if request.method == 'POST':
            create_serializer = self.get_serializer(
                data={'user': follower.id,
                      'following': id}
            )
            create_serializer.is_valid(raise_exception=True)
            create_serializer.save()
            serializer = serializers.FollowResponseSerializer(
                instance=following,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            follow = get_object_or_404(
                models.Follow, user=follower, following=following)
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['get'], detail=False)
    def subscriptions(self, request, *args, **kwargs):
        queryset = models.User.objects.filter(following__user=request.user)
        follows = self.paginate_queryset(queryset)
        serializer = serializers.FollowResponseSerializer(
            follows, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    def activation(self, request, *args, **kwargs):
        pass

    def resend_activation(self, request, *args, **kwargs):
        pass

    def reset_password(self, request, *args, **kwargs):
        pass

    def reset_password_confirm(self, request, *args, **kwargs):
        pass

    def reset_username(self, request, *args, **kwargs):
        pass

    def reset_username_confirm(self, request, *args, **kwargs):
        pass

    def set_username(self, request, *args, **kwargs):
        pass
