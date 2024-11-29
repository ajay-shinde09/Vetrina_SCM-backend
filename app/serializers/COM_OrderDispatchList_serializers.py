from rest_framework import serializers

class COMCustomerOrderListDispatchSerializer(serializers.Serializer):
    sr_no = serializers.IntegerField()  # Sr.No field will be handled manually
    customer_name = serializers.CharField(max_length=255)
    customer_role = serializers.CharField(max_length=255)
    order_date = serializers.DateTimeField()
    status = serializers.CharField(max_length=2)
    dispatch_date = serializers.DateTimeField()
