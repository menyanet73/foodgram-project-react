from rest_framework import mixins, generics


class FollowViewset(mixins.CreateModelMixin,
                    generics.GenericAPIView):
    pass