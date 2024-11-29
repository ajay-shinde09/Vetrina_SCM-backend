from rest_framework import serializers

class BatchDropdownSerializer(serializers.Serializer):
    batch_qty = serializers.CharField()
    product_id = serializers.IntegerField()
    Rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    MRP = serializers.DecimalField(max_digits=10, decimal_places=2)
