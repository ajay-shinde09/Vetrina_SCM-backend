from rest_framework import serializers

class ActiveCustomerListSerializer(serializers.Serializer):
    sr_no = serializers.IntegerField()
    customer_id = serializers.IntegerField()
    name = serializers.CharField()
    owner_name = serializers.CharField()
    email = serializers.EmailField()
    mobile_number = serializers.CharField()
    created_on = serializers.DateTimeField()
    actions = serializers.CharField()
