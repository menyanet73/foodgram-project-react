from rest_framework import mixins, viewsets

class CreateListRetrieveViewset(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    pass