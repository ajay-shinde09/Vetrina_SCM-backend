from rest_framework import serializers

class VetzoneGoodsSerializer(serializers.Serializer):
    sr_no = serializers.IntegerField()
    vetzone_name = serializers.CharField()
    hq = serializers.CharField()  
    mobile_number = serializers.CharField()
    sim_number = serializers.IntegerField()
    opening_goods = serializers.CharField()
    machine = serializers.CharField()
    furniture = serializers.CharField()
    furniture_file = serializers.CharField()
    machine_file = serializers.CharField()
    vetzone_agreement_copy = serializers.CharField()