from rest_framework import serializers

class VzOrdersCancelledSerializer(serializers.Serializer):
    sr_no = serializers.IntegerField()
    vetzone_name = serializers.CharField()
    order_date = serializers.DateTimeField()
    status = serializers.CharField()
    action = serializers.SerializerMethodField()

    def get_action(self, obj):
        # Create the action URL using the `stockiest_order_id`
        return f'/app/order-details-cancelled/{obj["stockiest_order_id"]}/'
 