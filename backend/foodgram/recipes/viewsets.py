from rest_framework import mixins, viewsets


class ReadOnlyViewset(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    pass