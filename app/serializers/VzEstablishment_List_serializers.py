from rest_framework import serializers

class VzEstablishmentListSerializer(serializers.Serializer):
    srno = serializers.IntegerField()
    vetzone_name = serializers.CharField(max_length=255)
    hq = serializers.CharField(max_length=255)
    contact_number = serializers.CharField(max_length=20)
    establishment = serializers.CharField(max_length=50) 