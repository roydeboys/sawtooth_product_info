from rest_framework import  serializers


class ProductSerializer(serializers.Serializer):
    Id = serializers.CharField()
    Name = serializers.CharField()
    ProductCode = serializers.CharField()
    attributes = serializers.JSONField()