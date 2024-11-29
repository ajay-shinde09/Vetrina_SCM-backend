from rest_framework import serializers

class CustomerRoleSerializer(serializers.Serializer):
    cust_role_id = serializers.IntegerField()
    role_name = serializers.CharField(max_length=255)
