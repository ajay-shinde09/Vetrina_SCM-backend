# # serializers.py
# from rest_framework import serializers

# class ComBatchAllocatedDetailsSerializer(serializers.Serializer):
#     customer_name = serializers.CharField()
#     order_id = serializers.IntegerField()
#     payment_method = serializers.CharField(required=False, allow_blank=True)

#     product_id = serializers.IntegerField()
#     Sr = serializers.IntegerField()
#     Product = serializers.CharField()
#     SKU = serializers.CharField()
#     Batch = serializers.CharField(allow_blank=True, default="")
#     Qty = serializers.IntegerField()
#     FreeQty = serializers.IntegerField()
#     MRP = serializers.FloatField()
#     Rate = serializers.FloatField()
#     Sale = serializers.CharField(allow_blank=True, default="")
#     AvailableQty = serializers.CharField(allow_blank=True, default="")
#     MIQ = serializers.CharField(allow_blank=True, default="")
#     Act = serializers.CharField(allow_blank=True, default="")

from rest_framework import serializers

class ProductDetailsSerializer(serializers.Serializer):
    SrNo = serializers.IntegerField()
    Product = serializers.CharField()
    SKU = serializers.CharField()
    Batch = serializers.CharField(allow_blank=True, default="")
    Qty = serializers.IntegerField()
    FreeQty = serializers.IntegerField()
    MRP = serializers.FloatField()
    Rate = serializers.FloatField()
    Sale = serializers.CharField(allow_blank=True, default="")
    AvailableQty = serializers.CharField(allow_blank=True, default="")
    MIQ = serializers.CharField(allow_blank=True, default="")
    Act = serializers.CharField(allow_blank=True, default="")
    product_id = serializers.IntegerField()
    user_id = serializers.IntegerField()


class CustomerDetailsSerializer(serializers.Serializer):
    customer_name = serializers.CharField()
    order_id = serializers.IntegerField()
    payment_method = serializers.CharField(required=False, allow_blank=True)


class ComBatchAllocatedDetailsSerializer(serializers.Serializer):
    customer_details = CustomerDetailsSerializer()
    product_details = ProductDetailsSerializer(many=True)
