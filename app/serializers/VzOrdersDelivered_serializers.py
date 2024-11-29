from rest_framework import serializers

class VzOrdersDeliveredSerializer(serializers.Serializer):
    sr_no = serializers.IntegerField()
    vetzone_name = serializers.CharField()
    order_date = serializers.DateTimeField()
    status = serializers.CharField()
    dispatch_date = serializers.DateTimeField()  # This can be filled with actual dispatch date
    action = serializers.SerializerMethodField()

    def get_action(self, obj):
        # Create the action URL using the `stockiest_order_id`
        return f'/app/order-details-delivered/{obj["stockiest_order_id"]}/'
