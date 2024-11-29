# from rest_framework import serializers

# class CreditPaymentOrders_Dispatchedserializers(serializers.Serializer):
#     sr_no = serializers.IntegerField()
#     OrderId = serializers.CharField(max_length=255)
#     customer_name = serializers.CharField(max_length=255)
#     customer_role = serializers.CharField(max_length=255)
#     order_date = serializers.DateTimeField()
#     dispatch_date = serializers.DateTimeField()
#     status = serializers.CharField(max_length=50)
#     lrno = serializers.CharField(allow_blank=True, required=False)  # Allow blank for LR number
#     file_url = serializers.URLField(allow_blank=True,allow_null=True)   # URL field for file path
#     action = serializers.DictField()  # Assuming action is a dictionary

#     class Meta:
#         fields = ['sr_no', 'OrderId','customer_name', 'customer_role', 'order_date', 'dispatch_date', 'status', 'lrno', 'file_path', 'action']
from rest_framework import serializers

class CustomerOrderSerializer(serializers.Serializer):
    OrderId = serializers.CharField()
    customer_name = serializers.CharField()
    customer_role = serializers.CharField()
    order_date = serializers.DateTimeField()
    dispatch_date = serializers.DateTimeField()
    status = serializers.CharField()
    file_path = serializers.CharField(allow_blank=True, required=False)
    sr_no = serializers.IntegerField()
    action = serializers.DictField()
    file_url = serializers.URLField(allow_blank=True, required=False)
class ProductDetailSerializer(serializers.Serializer):
    SrNo = serializers.IntegerField()
    CustomerName = serializers.CharField()
    OrderId = serializers.CharField()
    PaymentMode = serializers.CharField()
    HSNNumber = serializers.CharField()
    ProductName = serializers.CharField()
    SKU = serializers.CharField()
    Batch = serializers.CharField()
    Quantity = serializers.IntegerField()
    MRP = serializers.DecimalField(max_digits=10, decimal_places=2)
    Rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    Total = serializers.DecimalField(max_digits=10, decimal_places=2)
class OrderProductsSerializer(serializers.Serializer):
    common = serializers.DictField()  # Handles the common section
    details = serializers.ListField(child=serializers.DictField())  # Handles the list of products

class CreditPaymentOrders_DispatchedResponseSerializer(serializers.Serializer):
    customer_orders = serializers.ListField(child=serializers.DictField())  # List of orders
    order_products = OrderProductsSerializer()  # Use the updated serializer for order_products

