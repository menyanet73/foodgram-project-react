from rest_framework import mixins, viewsets


class FollowViewset(mixins.CreateModelMixin,
                    # mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    pass