from rest_framework import serializers

class AdminCustomerApprovalDetailSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    firm_name = serializers.CharField(allow_null=True, allow_blank=True)
    distributor_type = serializers.CharField(allow_null=True, allow_blank=True)
    headquarter = serializers.CharField(allow_blank=True)
    division = serializers.CharField(allow_null=True, allow_blank=True)
    kyc_status = serializers.CharField(allow_null=True, allow_blank=True)
    role_name = serializers.CharField(allow_null=True, allow_blank=True)

    customer_id = serializers.IntegerField()
    cust_name = serializers.CharField(allow_null=True, allow_blank=True)
    email = serializers.CharField(allow_null=True, allow_blank=True)
    cust_role = serializers.CharField(allow_null=True, allow_blank=True)
    stockiest_type = serializers.CharField(allow_null=True, allow_blank=True)
    addressl1 = serializers.CharField(allow_null=True, allow_blank=True)
    addressl2 = serializers.CharField(allow_null=True, allow_blank=True)
    taluka = serializers.CharField(allow_null=True, allow_blank=True)
    District = serializers.CharField(allow_null=True, allow_blank=True)
    State = serializers.CharField(allow_null=True, allow_blank=True)
    Pin_code = serializers.CharField(allow_null=True, allow_blank=True)
    mob_no = serializers.CharField(allow_null=True, allow_blank=True)
    geo_tag = serializers.CharField(allow_null=True, allow_blank=True)
    date_of_establishment = serializers.CharField(allow_null=True, allow_blank=True)
    gst_no = serializers.CharField(allow_null=True, allow_blank=True)
    pan_no = serializers.CharField(allow_null=True, allow_blank=True)
    drug_licence_no = serializers.CharField(allow_null=True, allow_blank=True)
    from_date = serializers.CharField(allow_null=True, allow_blank=True)
    to_date = serializers.CharField(allow_null=True, allow_blank=True)
    bank_name = serializers.CharField(allow_null=True, allow_blank=True)
    bank_ac_no = serializers.CharField(allow_null=True, allow_blank=True)
    bank_ifsc = serializers.CharField(allow_null=True, allow_blank=True)
    bank_address = serializers.CharField(allow_null=True, allow_blank=True)
    anual_turnover = serializers.CharField(allow_null=True, allow_blank=True)
    no_of_company = serializers.CharField(allow_null=True, allow_blank=True)
    area_state = serializers.CharField(allow_null=True, allow_blank=True)
    area_district = serializers.CharField(allow_null=True, allow_blank=True)
    expected_anual_business = serializers.CharField(allow_null=True, allow_blank=True)
    contact_person_name = serializers.CharField(allow_null=True, allow_blank=True)
    contact_person_mobile = serializers.CharField(allow_null=True, allow_blank=True)
    contact_person_email = serializers.CharField(allow_null=True, allow_blank=True)
    submit = serializers.CharField(allow_null=True, allow_blank=True)
    kyc_documents = serializers.ListField(
        child=serializers.DictField(), required=False
    )



    class Meta:
        fields = [
            'customer_id', 'firm_name', 'distributor_type', 'headquarter', 
            'division', 'kyc_status', 'role_name','customer_id', 'cust_name', 'email', 'cust_role', 'stockiest_type', 'addressl1', 'addressl2', 
            'hq', 'division', 'subDivision', 'vsoname', 'vsomob', 'taluka', 'District', 'State', 'Pin_code',
            'mob_no', 'geo_tag', 'date_of_establishment', 'gst_no', 'pan_no', 'drug_licence_no', 'from_date', 
            'to_date', 'bank_name', 'bank_ac_no', 'bank_ifsc', 'bank_address', 'anual_turnover', 'no_of_company', 
            'area_state', 'area_district', 'expected_anual_business', 'contact_person_name', 'contact_person_mobile', 
            'contact_person_email', 'supplier', 'cnf', 'update_customer','credit_days', 'credit_limit','kyc_documents'
        ]