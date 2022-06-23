from base64 import b64decode
from uuid import uuid4

from django.core.files.base import ContentFile
from rest_framework import serializers


class ImageSerializerField(serializers.ImageField):

    def to_internal_value(self, data):
        try:
            header, body = data.split(';base64,')
            file_format = header.split('image/')[-1]
            name = f'recipes/images/{uuid4()}.{file_format}'
            data = ContentFile(b64decode(body), name)
        except (ValueError, KeyError):
            raise serializers.ValidationError('Wrong image data')
        return super().to_internal_value(data)
