from rest_framework import serializers

class OrderDetailsSerializer(serializers.Serializer):
    sr_no = serializers.IntegerField()
    order_no = serializers.IntegerField()
    vetzone_name = serializers.CharField(max_length=255)
    headquarters = serializers.CharField(max_length=255)
    order_date = serializers.DateTimeField()
    amount = serializers.FloatField()
    status = serializers.CharField(max_length=2)

class ProductDetailsSerializer(serializers.Serializer):
    sr_no = serializers.IntegerField()
    product_name = serializers.CharField(max_length=255)
    sku = serializers.CharField(max_length=255)
    quantity = serializers.IntegerField()
    mrp = serializers.FloatField()
    rate = serializers.FloatField()
