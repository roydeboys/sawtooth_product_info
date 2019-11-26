from rest_framework import  serializers
from .models import BlockInfo


class BlockInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockInfo
        exclude = ('id', )