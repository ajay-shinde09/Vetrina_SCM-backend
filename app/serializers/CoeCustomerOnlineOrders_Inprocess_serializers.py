from rest_framework import serializers

class CoeCustomerOnlineOrdersInprocessserializers(serializers.Serializer):
    sr_no = serializers.IntegerField()
    order_id = serializers.IntegerField()
    customer_name = serializers.CharField(max_length=100)
    customer_role = serializers.CharField(max_length=100)
    order_date = serializers.DateTimeField()
    status = serializers.CharField(max_length=50)
    dispatch_date = serializers.CharField(default="Not Dispatched")
    action = serializers.DictField(child=serializers.CharField())
    
class CoeCustomerLrUploadSerializer(serializers.Serializer):
    lr_number = serializers.CharField(max_length=20, required=True)  # Ensure this is required
    receipt_file = serializers.FileField(required=True)  # Ensure this is required