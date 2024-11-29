from rest_framework import serializers

class VzOrdersPendingSerializer(serializers.Serializer):
    sr_no = serializers.IntegerField()
    vetzone_name = serializers.CharField()
    order_date = serializers.DateTimeField()
    status = serializers.CharField()
    action = serializers.SerializerMethodField()

    def get_action(self, obj):
        return f'/app/order-details-pending/{obj["order_id"]}/'  # Access using the key
