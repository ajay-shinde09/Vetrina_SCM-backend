from rest_framework import serializers

# class CoeCustomerOnlineOrdersDispatchedserializers(serializers.Serializer):
#     sr_no = serializers.IntegerField()
#     customer_name = serializers.CharField(max_length=255)
#     customer_role = serializers.CharField(max_length=255)
#     order_date = serializers.DateTimeField()
#     dispatch_date = serializers.DateTimeField()
#     status = serializers.CharField(max_length=50)
#     lrno = serializers.CharField(allow_blank=True, required=False)  # Allow blank for LR number
#     file_path = serializers.URLField(allow_blank=True)    # URL field for file path
#     action = serializers.DictField()  # Assuming action is a dictionary

#     class Meta:
#         fields = ['sr_no', 'customer_name', 'customer_role', 'order_date', 'dispatch_date', 'status', 'lrno', 'file_path', 'action']
class CoeCustomerOnlineOrdersDispatchedserializers(serializers.Serializer):
    sr_no = serializers.IntegerField()
    customer_name = serializers.CharField(max_length=255)
    customer_role = serializers.CharField(max_length=255)
    order_date = serializers.DateTimeField()
    dispatch_date = serializers.DateTimeField()
    status = serializers.CharField(max_length=50)
    lrno = serializers.CharField(allow_blank=True, required=False)  # Allow blank for LR number
    file_path = serializers.CharField(allow_blank=True, required=False)  # Allow plain file names
    file_url = serializers.URLField(allow_blank=True, required=False)   # URL for the full file path
    action = serializers.DictField()  # Assuming action is a dictionary

    class Meta:
        fields = [
            'sr_no', 'customer_name', 'customer_role', 'order_date', 
            'dispatch_date', 'status', 'lrno', 'file_path', 'file_url', 'action'
        ]