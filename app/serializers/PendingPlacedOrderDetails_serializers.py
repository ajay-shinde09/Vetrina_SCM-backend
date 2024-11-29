from rest_framework import serializers

class PendingPlacedOrderDetailsSerializer(serializers.Serializer):
    customer_name = serializers.CharField(required=False, allow_null=True, default=None)
    order_id = serializers.IntegerField(required=False, allow_null=True, default=None)
    payment_method = serializers.CharField(required=False, allow_blank=True, allow_null=True, default=None)

    product_id = serializers.IntegerField(required=False, allow_null=True, default=None)
    user_role= serializers.CharField(required=False, allow_blank=True, default="")
    user_id= serializers.IntegerField(required=False, allow_null=True, default=None)
    order_id= serializers.IntegerField(required=False, allow_null=True, default=None)
    scheme_name= serializers.CharField(required=False, allow_blank=True, default="")
    Sr = serializers.IntegerField(required=False, allow_null=True, default=None)
    Product = serializers.CharField(required=False, allow_blank=True, default="")
    SKU = serializers.CharField(required=False, allow_blank=True, default="")
    Batch = serializers.CharField(required=False, allow_blank=True, default="")
    Qty = serializers.IntegerField(required=False, allow_null=True, default=None)
    FreeQty = serializers.IntegerField(required=False, allow_null=True, default=None)
    MRP = serializers.FloatField(required=False, allow_null=True, default=None)
    Rate = serializers.FloatField(required=False, allow_null=True, default=None)
    Sale = serializers.CharField(required=False, allow_blank=True, default="")
    AvailableQty = serializers.CharField(required=False, allow_blank=True, default="")
    MIQ = serializers.CharField(required=False, allow_blank=True, default="")
    Act = serializers.CharField(required=False, allow_blank=True, default="")
