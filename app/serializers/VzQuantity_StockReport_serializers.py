from rest_framework import serializers

class VetZoneStockReportSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=100)
    sku = serializers.CharField(max_length=100)
    batch_number = serializers.CharField(max_length=100)
    available_quantity = serializers.IntegerField()
