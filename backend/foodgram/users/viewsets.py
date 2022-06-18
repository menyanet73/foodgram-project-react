from rest_framework import mixins, viewsets


class FollowViewset(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    pass