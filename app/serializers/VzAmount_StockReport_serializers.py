# app/serializers.py
from rest_framework import serializers

class VetzoneStockSerializer(serializers.Serializer):
    sr_no = serializers.IntegerField()
    product_name = serializers.CharField()
    sku = serializers.CharField()
    batch = serializers.CharField()
    amount = serializers.FloatField()
