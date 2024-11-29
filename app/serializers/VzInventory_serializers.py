from rest_framework import serializers

class VetzoneProductSerializer(serializers.Serializer):
    sr_no = serializers.IntegerField()
    product_name = serializers.CharField(max_length=255)
    sku = serializers.CharField(max_length=13)
    product_code = serializers.IntegerField()
    available_quantity = serializers.CharField(allow_blank=True)  # Empty for now

# serializers.py
from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    sku = serializers.CharField()
    product_code = serializers.IntegerField()
    available_qty = serializers.IntegerField()  # Add available_qty field
