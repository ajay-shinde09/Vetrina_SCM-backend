from rest_framework import serializers

class ProductDetailSerializer(serializers.Serializer):
    sr_no = serializers.IntegerField()
    hsn_code = serializers.IntegerField()
    product_name = serializers.CharField()
    sku = serializers.CharField()
    batch = serializers.CharField()
    expiry_date = serializers.DateTimeField()
    quantity = serializers.IntegerField()
    free = serializers.IntegerField()
    mrp = serializers.CharField()
    pts = serializers.DecimalField(max_digits=7, decimal_places=2)
    ptr = serializers.DecimalField(max_digits=6, decimal_places=2)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)  # Use DecimalField instead of FloatField
    disc = serializers.DecimalField(max_digits=5, decimal_places=2)  # Change to DecimalField
    taxable = serializers.DecimalField(max_digits=10, decimal_places=2)  # Change to DecimalField

    # Conditional GST fields
    IGST_per = serializers.DecimalField(max_digits=5, decimal_places=2)  # Change to DecimalField
    CGST_per = serializers.DecimalField(max_digits=5, decimal_places=2)  # Change to DecimalField
    SGST_per = serializers.DecimalField(max_digits=5, decimal_places=2)  # Change to DecimalField
    IGST_Amt = serializers.DecimalField(max_digits=10, decimal_places=2)  # Change to DecimalField
    CGST_Amt = serializers.DecimalField(max_digits=10, decimal_places=2)  # Change to DecimalField
    SGST_Amt = serializers.DecimalField(max_digits=10, decimal_places=2)  # Change to DecimalField

    discounted_amount=serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)


class CustomerinvoiceSerializer(serializers.Serializer):
    name = serializers.CharField()
    mobile = serializers.CharField()
    address = serializers.CharField()
    taluka = serializers.CharField()
    district = serializers.CharField()
    state = serializers.CharField()
    state_name  = serializers.CharField()
    state_id = serializers.IntegerField()  # Added state_id field
    state_code = serializers.IntegerField()  
    pincode = serializers.CharField()
    gstin = serializers.CharField(allow_null=True, required=False)
    pan = serializers.CharField()
    bank_name = serializers.CharField()
    account_no = serializers.CharField()
    invoice_no = serializers.CharField()
    invoice_date = serializers.DateTimeField()
    order_id = serializers.IntegerField()
    placeorder_date = serializers.DateTimeField()
    bank_ifsc = serializers.CharField()
    drug_licence_no = serializers.CharField()
    invoice_amount=serializers.IntegerField()

    products = ProductDetailSerializer(many=True)
    invoice_amount_words = serializers.CharField(read_only=True)
    less = serializers.DecimalField(max_digits=10, decimal_places=2) 
    bill_total = serializers.DecimalField(max_digits=10, decimal_places=2) 
    total_gst_I= serializers.DecimalField(required=False, default=0.0, max_digits=10, decimal_places=2)
    total_CGST_Amt=serializers.DecimalField(max_digits=10, decimal_places=2) 
    total_SGST_Amt=serializers.DecimalField(max_digits=10, decimal_places=2) 
    total_gst_cs = serializers.DecimalField(required=False, default=0.0, max_digits=10, decimal_places=2)
    NET_AMT_cs=serializers.DecimalField(required=False, default=0.0, max_digits=10, decimal_places=2)
    NET_AMT_i=serializers.DecimalField(required=False, default=0.0, max_digits=10, decimal_places=2)

    net_amt = serializers.FloatField()
    net_amt_words = serializers.CharField()




    # 23904-717.12