from rest_framework import serializers

class VetZoneGoodsSerializer(serializers.Serializer):
    vetzone_id = serializers.IntegerField()
    vetzone_name = serializers.CharField(max_length=255)
    sim_number = serializers.IntegerField()
    opening_goods = serializers.CharField(max_length=255)
    machine = serializers.CharField(max_length=255)
    machine_file = serializers.CharField(max_length=255, allow_blank=True)
    furniture = serializers.CharField(max_length=255)
    furniture_file = serializers.CharField(max_length=255, allow_blank=True)
