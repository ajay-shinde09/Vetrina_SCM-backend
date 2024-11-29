from rest_framework import serializers

class CeoCustomerApprovalListSerializer(serializers.Serializer):
    sr_no = serializers.IntegerField()
    customer_id = serializers.IntegerField()
    firm_name = serializers.CharField(max_length=255)
    role = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    mobile_number = serializers.CharField(max_length=15)
    registration_date = serializers.DateTimeField()
    approval_status = serializers.CharField(max_length=10)
    action_link = serializers.URLField()  # Add this line to include action_link
