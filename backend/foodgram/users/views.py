from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from users import models, serializers, viewsets


class UserViewSet(viewsets.UsersViewSet):
    queryset = models.User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'set_password':
            return serializers.SetPasswordSerializer
        if self.action in ['subscribe', 'subscriptions']:
            return serializers.FollowSerializer
        return serializers.UsersSerializer

    @action(['get'], detail=False)
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['post', 'delete'], detail=True)
    def subscribe(self, request, pk, *args, **kwargs):
        follower = request.user
        following = get_object_or_404(models.User, id=pk)
        if request.method == 'POST':
            create_serializer = self.get_serializer(
                data={'user': follower.id,
                      'following': pk}
            )
            create_serializer.is_valid(raise_exception=True)
            create_serializer.save()
            serializer = serializers.FollowResponseSerializer(
                instance=following,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(['get'], detail=False)
    def subscriptions(self, request, *args, **kwargs):
        queryset = models.User.objects.filter(following__user=request.user)
        follows = self.paginate_queryset(queryset)
        serializer = serializers.FollowResponseSerializer(
            follows, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
