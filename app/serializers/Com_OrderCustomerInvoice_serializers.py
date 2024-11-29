from rest_framework import serializers


#     # 23904-717.12
class ComBatchAllocatedInvoiceSerializer(serializers.Serializer):
    name = serializers.CharField()
    mobile = serializers.CharField()
    address = serializers.CharField()
    taluka = serializers.CharField()
    district = serializers.CharField()
    state = serializers.CharField()
    state_id = serializers.IntegerField()
    state_name  = serializers.CharField()
    state_code = serializers.IntegerField()
    pincode = serializers.CharField()
    gstin = serializers.CharField(allow_null=True, required=False)
    pan = serializers.CharField()
    bank_name = serializers.CharField()
    account_no = serializers.CharField()
    order_id = serializers.IntegerField()
    placeorder_date = serializers.DateTimeField()
    bank_ifsc = serializers.CharField()
    drug_licence_no = serializers.CharField()
    invoice_no= serializers.CharField()

    # Add a nested serializer for product details
    products = serializers.ListField(
        child=serializers.DictField()
    )
    
    # Additional fields to handle dynamic calculations
    less = serializers.DecimalField(max_digits=10, decimal_places=2)
    bill_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_CGST_Amt = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_SGST_Amt = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_gst_cs = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_gst_I = serializers.DecimalField(max_digits=10, decimal_places=2)
    # NET_AMT_cs = serializers.DecimalField(max_digits=10, decimal_places=2)
    # NET_AMT_i = serializers.DecimalField(max_digits=10, decimal_places=2)
    NET_AMT_cs = serializers.IntegerField()
    NET_AMT_i = serializers.IntegerField()
    NET_AMT_cs_words = serializers.CharField()
    NET_AMT_i_words = serializers.CharField()

    # New fields for net amount and words
    net_amt = serializers.IntegerField()
    net_amt_words = serializers.CharField()

