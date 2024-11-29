from rest_framework import serializers

class DistributorTypeSerializer(serializers.Serializer):
    distributor_type_id = serializers.IntegerField()
    distributor_type = serializers.CharField(max_length=255)
