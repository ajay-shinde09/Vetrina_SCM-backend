# serializers.py
from rest_framework import serializers

class ComPendingCustomerOrderListSerializer(serializers.Serializer):
    sr_no = serializers.IntegerField()
    customer_name = serializers.CharField()
    customer_role = serializers.CharField()
    order_date = serializers.DateTimeField()
    status = serializers.CharField()
    action = serializers.URLField()
