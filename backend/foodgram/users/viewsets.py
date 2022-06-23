from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class UsersViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    pass
