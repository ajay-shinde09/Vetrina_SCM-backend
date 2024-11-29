# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    username = models.TextField(unique=True)
    admin_email = models.TextField(unique=True)
    password = models.TextField()
    line_manager = models.IntegerField()
    permission_id = models.IntegerField()
    created_by = models.IntegerField()
    created_date = models.DateTimeField()
    status = models.CharField(max_length=1)
    is_block = models.CharField(max_length=1)
   
    USERNAME_FIELD = 'admin_email'
    REQUIRED_FIELDS = []
    # def is_authenticated(self):
    #     return True
    @property
    def is_anonymous(self):
        return False  # Since this is an actual user, it is not anonymous
    @property
    def is_active(self):
        return True  # Since this is an actual user, it is not anonymous

    @property
    def is_authenticated(self):
        return True  # If this object is created, it's an authenticated user

    class Meta:
        managed = False
        db_table = 'admin'
        


class AdminHqDiv(models.Model):
    admin_hq_div_id = models.AutoField(primary_key=True)
    admin_id = models.IntegerField()
    hq_id = models.IntegerField()
    div_id = models.IntegerField()
    sub_division = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin_hq_div'


class AdminMeta(models.Model):
    ad_meta_id = models.AutoField(primary_key=True)
    admin_id = models.IntegerField()
    address = models.TextField()
    taluka = models.TextField()
    district = models.TextField()
    state = models.TextField()
    pin_code = models.IntegerField()
    geo_location = models.TextField(blank=True, null=True)
    emp_id = models.TextField()
    mob_number_company = models.TextField()
    mob_number_personal = models.TextField()
    vetzone = models.IntegerField()
    profile_pic = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin_meta'


class AdminRoles(models.Model):
    role_id = models.AutoField(primary_key=True)
    admin_id = models.IntegerField()
    desig_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'admin_roles'


class AdvancePaymentDetails(models.Model):
    payment_id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    order_id = models.IntegerField()
    amount = models.TextField()
    transcation_id = models.TextField()
    reciept = models.TextField()
    payment_date = models.DateTimeField()
    payment_mode = models.TextField()
    status = models.CharField(max_length=1, db_comment='P -pendingApproval\r\nY - Accepted\r\nD - Rejected')

    class Meta:
        managed = False
        db_table = 'advance_payment_details'


class Batch(models.Model):
    batch_id = models.AutoField(primary_key=True)
    batch = models.TextField()
    product_id = models.IntegerField()
    good_reciept_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'batch'


class Comission(models.Model):
    comission_id = models.AutoField(primary_key=True)
    vetzone_id = models.IntegerField()
    commission = models.IntegerField()
    tds = models.IntegerField()
    commission_amt = models.IntegerField()
    status = models.CharField(max_length=11)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'comission'


class ComissionApproveHold(models.Model):
    comission_aphold_id = models.AutoField(primary_key=True)
    vetzone_id = models.IntegerField()
    comission = models.IntegerField()
    tds = models.IntegerField()
    commission_amt = models.IntegerField()
    status = models.CharField(max_length=1, db_comment='P: Proceed to Pay; U: Unpaid; H: Hold')
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'comission_approve_hold'


class CreditNoteTable(models.Model):
    credit_note_id = models.AutoField(primary_key=True)
    amount = models.TextField()
    invoice_date = models.DateTimeField()
    order_id = models.IntegerField()
    user_id = models.IntegerField()
    user_role = models.TextField()
    order_date = models.DateField()
    credit_end_date = models.DateField()
    payment_status = models.CharField(max_length=1)
    payment_date = models.DateField()
    placeorder = models.CharField(max_length=1)
    comment = models.TextField()

    class Meta:
        managed = False
        db_table = 'credit_note_table'


class CreditNoteUserDetails(models.Model):
    credit_note_user_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    credit_limit = models.TextField()
    credit_days = models.TextField()

    class Meta:
        managed = False
        db_table = 'credit_note_user_details'


class CreditNotes(models.Model):
    credit_note_id = models.AutoField(primary_key=True)
    credit_note_no = models.TextField()
    return_id = models.IntegerField()
    cust_type = models.TextField()
    credit_amount = models.FloatField()
    created_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'credit_notes'


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    owner_name = models.TextField(blank=True, null=True)
    mobile_number = models.TextField()
    email = models.TextField()
    password = models.TextField()
    type = models.IntegerField()
    role = models.IntegerField()
    kyc_status = models.CharField(max_length=1)
    approval_status = models.CharField(max_length=1, db_comment='Y -> Approved N -> Declined P->Pending A->Approved by Admin F->Approved by Finance')
    is_block = models.CharField(max_length=1)
    created_on = models.DateTimeField()
    placeorder = models.CharField(max_length=1)
    state_id = models.IntegerField()
    remark = models.TextField(blank=True, null=True)
    terms_conditions = models.CharField(max_length=1, db_comment='N - Accepted on Registration\r\nY- Accepted on Mail')
    supplier = models.IntegerField(blank=True, null=True)
    farmer_type = models.CharField(max_length=11, blank=True, null=True)
    dairy_animals = models.IntegerField(blank=True, null=True)
    sheep_goat = models.IntegerField(blank=True, null=True)
    piggery_animals = models.IntegerField(blank=True, null=True)
    layer_birds = models.IntegerField(blank=True, null=True)
    broiler_birds = models.IntegerField(blank=True, null=True)
    reference = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'


class CustomerHqDiv(models.Model):
    customer_hq_div_id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    hq_id = models.IntegerField()
    div_id = models.IntegerField()
    approval_admin_id = models.IntegerField()
    sub_division = models.TextField()

    class Meta:
        managed = False
        db_table = 'customer_hq_div'


class CustomerInstock(models.Model):
    instock_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    product_id = models.IntegerField()
    sku = models.TextField()
    quantity = models.IntegerField()
    batch = models.TextField()
    manfacturing_date = models.DateField()
    expiry_date = models.DateField()
    mrp = models.FloatField()
    purchase_rate = models.FloatField()
    pts = models.FloatField()
    ptr = models.FloatField()
    ptc = models.FloatField()
    ptv = models.FloatField()
    ptk = models.FloatField()
    margin = models.FloatField()
    created_by = models.IntegerField()
    created_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'customer_instock'


class CustomerInvoice(models.Model):
    customer_invoice_id = models.AutoField(primary_key=True)
    invoice_no = models.TextField()
    order_id = models.IntegerField()
    invoice_amount = models.IntegerField()
    created_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'customer_invoice'


class CustomerKycDocument(models.Model):
    cust_kyc_id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    document = models.TextField(blank=True, null=True)
    approval_satatus = models.CharField(max_length=1)
    uploaded_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'customer_kyc_document'


class CustomerLrDetails(models.Model):
    lr_detail_id = models.AutoField(primary_key=True)
    lrno = models.TextField()
    order_id = models.IntegerField()
    file = models.TextField()
    is_verified = models.CharField(max_length=1)
    dispatch_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'customer_lr_details'


class CustomerMeta(models.Model):
    customer_meta_id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    customer_meta_key = models.TextField(blank=True, null=True)
    customer_meta_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_meta'


class CustomerNotification(models.Model):
    notify_id = models.AutoField(primary_key=True)
    send_form_id = models.IntegerField()
    send_to_id = models.IntegerField()
    notification_text = models.TextField(blank=True, null=True)
    its_view = models.CharField(max_length=1)
    its_click = models.CharField(max_length=1)
    notifiedtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'customer_notification'


class CustomerOrderTableProduct(models.Model):
    order_product_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    product_id = models.IntegerField()
    batch = models.TextField(blank=True, null=True)
    rate = models.FloatField()
    disc = models.FloatField()
    tax = models.FloatField()
    mrp = models.FloatField()
    rate_mode = models.TextField(blank=True, null=True)
    quantity = models.IntegerField()
    free = models.IntegerField()
    scheme_name = models.TextField(blank=True, null=True)
    customer_id = models.IntegerField()
    customer_type = models.TextField()
    seller_user_id = models.IntegerField()
    seller_user_role = models.TextField()
    status = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'customer_order_table_product'


class CustomerPlaceorder(models.Model):
    customer_order_id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField()
    status = models.CharField(max_length=2)
    is_invoiced = models.CharField(max_length=1)
    is_placed_order = models.CharField(max_length=1)
    user_id = models.IntegerField()
    user_role = models.TextField()
    order_type = models.CharField(max_length=10)
    payment_method = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_placeorder'


class CustomerReference(models.Model):
    reference_id = models.AutoField(primary_key=True)
    referencename = models.CharField(db_column='ReferenceName', max_length=250)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'customer_reference'


class CustomerRoles(models.Model):
    cust_role_id = models.AutoField(primary_key=True)
    role_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'customer_roles'


class DeliveryChallan(models.Model):
    delivery_challan_id = models.AutoField(primary_key=True)
    invoice_no = models.TextField()
    order_id = models.IntegerField()
    invoice_amount = models.FloatField()
    created_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'delivery_challan'


class Designations(models.Model):
    desig_id = models.AutoField(primary_key=True)
    desig_name = models.TextField()
    parent_desig_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'designations'


class DistributorType(models.Model):
    distributor_type_id = models.AutoField(primary_key=True)
    distributor_type = models.TextField()

    class Meta:
        managed = False
        db_table = 'distributor_type'


class District(models.Model):
    district_id = models.AutoField(primary_key=True)
    district_name = models.TextField()
    state_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'district'


class Divisions(models.Model):
    division_id = models.AutoField(primary_key=True)
    division_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'divisions'


class EndCustomer(models.Model):
    end_customer_id = models.AutoField(primary_key=True)
    created_by_user_id = models.IntegerField()
    created_by_user_role = models.IntegerField()
    created_date = models.DateTimeField()
    name = models.TextField(blank=True, null=True)
    mobile = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    farm_name = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    taluka = models.TextField(blank=True, null=True)
    district = models.TextField(db_column='District', blank=True, null=True)  # Field name made lowercase.
    state = models.TextField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    pin_code = models.TextField(db_column='Pin_code', blank=True, null=True)  # Field name made lowercase.
    gst_no = models.TextField(blank=True, null=True)
    hq = models.IntegerField()
    division = models.IntegerField()
    status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'end_customer'


class GoodReciept(models.Model):
    good_reciept_id = models.AutoField(primary_key=True)
    gr_no = models.IntegerField()
    challan_no = models.IntegerField()
    supplier = models.IntegerField()
    challan_date = models.DateField()
    created_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'good_reciept'


class GoodsReturnDetails(models.Model):
    return_id = models.AutoField(primary_key=True)
    goods_return_id = models.IntegerField()
    product_id = models.IntegerField()
    sku = models.TextField(blank=True, null=True)
    batch = models.TextField()
    manufacturing_date = models.DateField()
    expiry_date = models.DateField()
    mrp = models.FloatField()
    customer_id = models.IntegerField()
    type = models.TextField(blank=True, null=True)
    quantity = models.IntegerField()
    scheme_name = models.TextField(blank=True, null=True)
    rate = models.FloatField()
    netrate = models.FloatField(db_column='NetRate')  # Field name made lowercase.
    created_date = models.DateTimeField()
    action = models.CharField(max_length=2, blank=True, null=True, db_comment='RU - Reuse\r\nRP - Reprocess\r\nRO - RightOff')
    reuse = models.IntegerField(blank=True, null=True)
    reprocess = models.IntegerField(blank=True, null=True)
    rightoff = models.IntegerField(blank=True, null=True)
    isapproved = models.CharField(db_column='isApproved', max_length=1, blank=True, null=True)  # Field name made lowercase.
    remark = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'goods_return_details'


class Headquarters(models.Model):
    hq_id = models.AutoField(primary_key=True)
    hq_name = models.TextField()
    base_town = models.TextField(blank=True, null=True)
    base_town_id = models.IntegerField()
    geo_location = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'headquarters'


class Instock(models.Model):
    instock_id = models.AutoField(primary_key=True)
    good_reciept_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    sku = models.CharField(max_length=14, db_collation='utf8mb3_general_ci', blank=True, null=True)
    quantity = models.CharField(max_length=11, db_collation='utf8mb3_general_ci', blank=True, null=True)
    batch_id = models.IntegerField(blank=True, null=True)
    batch = models.CharField(max_length=11, db_collation='utf8mb3_general_ci', blank=True, null=True)
    manfacturing_date = models.CharField(max_length=19, db_collation='utf8mb3_general_ci', blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    mrp = models.CharField(max_length=19, db_collation='utf8mb3_general_ci', blank=True, null=True)
    purchase_rate = models.IntegerField(blank=True, null=True)
    pts = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    ptr = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ptc = models.IntegerField(blank=True, null=True)
    ptv = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    ptk = models.IntegerField(blank=True, null=True)
    margin = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'instock'


class Instock1(models.Model):
    instock_id = models.AutoField(primary_key=True)
    good_reciept_id = models.IntegerField()
    product_id = models.IntegerField()
    sku = models.TextField()
    quantity = models.IntegerField()
    batch_id = models.IntegerField()
    batch = models.TextField()
    manfacturing_date = models.DateField()
    expiry_date = models.DateField()
    mrp = models.FloatField()
    purchase_rate = models.FloatField()
    pts = models.FloatField()
    ptr = models.FloatField()
    ptc = models.FloatField()
    ptv = models.FloatField()
    ptk = models.FloatField()
    margin = models.FloatField()
    created_by = models.IntegerField()
    created_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'instock1'


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    invoice_no = models.TextField()
    order_id = models.IntegerField()
    invoice_amount = models.IntegerField()
    created_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'invoice'


class InvoiceDetails(models.Model):
    invoice_details_id = models.AutoField(primary_key=True)
    invoice_id = models.IntegerField()
    customer_id = models.IntegerField()
    product_id = models.IntegerField()
    batch = models.TextField()
    igst = models.IntegerField()
    sgst = models.IntegerField()
    cgst = models.IntegerField()
    quantity = models.IntegerField()
    rate = models.IntegerField()
    disc = models.IntegerField()
    taxble_amount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'invoice_details'


class LrDetails(models.Model):
    lr_detail_id = models.AutoField(primary_key=True)
    lrno = models.TextField(blank=True, null=True)
    order_id = models.IntegerField()
    file = models.TextField(blank=True, null=True)
    is_verified = models.CharField(max_length=1)
    dispatch_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'lr_details'


class MobileSingleDeviceStatus(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    user_id = models.IntegerField()
    user_email = models.CharField(max_length=100)
    user_type = models.CharField(max_length=50)
    device_id = models.CharField(max_length=50)
    modal_name = models.CharField(max_length=70)
    login_status = models.CharField(max_length=50)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mobile_single_device_status'


class MonthlyComissionPayable(models.Model):
    comission_payable_id = models.AutoField(primary_key=True)
    comission_meta_id = models.IntegerField()
    vetzone_id = models.IntegerField()
    commission_amt = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=11, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'monthly_comission_payable'


class Notification(models.Model):
    notify_id = models.AutoField(primary_key=True)
    send_form_id = models.IntegerField()
    send_to_id = models.IntegerField()
    notification_text = models.TextField(blank=True, null=True)
    its_view = models.CharField(max_length=1)
    its_click = models.CharField(max_length=1)
    notifiedtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'notification'


class OrderApproval(models.Model):
    order_approval_id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    order_id = models.IntegerField()
    from_admin_id = models.IntegerField()
    from_role_id = models.IntegerField()
    to_admin_id = models.IntegerField()
    to_role_id = models.IntegerField()
    action = models.CharField(max_length=25)
    on_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_approval'


class OrderTableProduct(models.Model):
    order_product_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    product_id = models.IntegerField()
    batch = models.TextField(blank=True, null=True)
    rate = models.FloatField()
    disc = models.FloatField()
    tax = models.FloatField()
    mrp = models.FloatField()
    rate_mode = models.TextField(blank=True, null=True)
    quantity = models.IntegerField()
    free = models.IntegerField()
    scheme_name = models.TextField(blank=True, null=True)
    user_id = models.IntegerField()
    user_role = models.TextField()
    status = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_table_product'


class OrderingHierarchy(models.Model):
    ordering_hierarchy_id = models.AutoField(primary_key=True)
    from_customer_id = models.IntegerField()
    from_admin_id = models.IntegerField()
    from_role_id = models.IntegerField()
    action = models.TextField()
    to_admin_id = models.IntegerField()
    to_role_id = models.IntegerField()
    payment_method = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ordering_hierarchy'


class PaymentDetails(models.Model):
    payment_id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    amount = models.TextField()
    transcation_id = models.TextField()
    reciept = models.TextField()
    payment_date = models.DateTimeField()
    payment_mode = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment_details'


class Placeorder(models.Model):
    stockiest_order_id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField()
    status = models.CharField(max_length=2, db_comment='P - Pending\r\nI - Inprocess\r\nY - Dispatched\r\nD - Delivered\r\nN - Cancelled\r\nA - Advanced\r\nPI - PI Generated\r\nPA - payment Acceptance\r\nF - For Approval at Finance')
    is_invoiced = models.CharField(max_length=1)
    is_placed_order = models.CharField(max_length=1)
    user_id = models.IntegerField()
    user_role = models.TextField()
    order_type = models.CharField(max_length=10)
    payment_method = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'placeorder'


class PricingStructure(models.Model):
    pricing_id = models.AutoField(primary_key=True)
    division_id = models.IntegerField()
    customer_type = models.IntegerField()
    file = models.TextField()
    created_on = models.DateTimeField()
    created_by = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pricing_structure'


class ProcessTable(models.Model):
    process_id = models.IntegerField()
    customer_id = models.IntegerField()
    from_desig_id = models.IntegerField()
    from_admin_id = models.IntegerField()
    to_desig_id = models.IntegerField()
    to_admin_id = models.IntegerField()
    action = models.TextField()
    remark = models.TextField()
    created_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'process_table'


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=27, db_collation='utf8mb3_general_ci', blank=True, null=True)
    sku = models.CharField(max_length=13, db_collation='utf8mb3_general_ci', blank=True, null=True)
    product_code = models.IntegerField(blank=True, null=True)
    unit = models.CharField(max_length=4, db_collation='utf8mb3_general_ci', blank=True, null=True)
    product_division = models.IntegerField(blank=True, null=True)
    sub_division = models.CharField(max_length=7, db_collation='utf8mb3_general_ci', blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)
    manufacturer = models.CharField(max_length=26, db_collation='utf8mb3_general_ci', blank=True, null=True)
    barcode = models.IntegerField(blank=True, null=True)
    shipper_size = models.CharField(max_length=17, db_collation='utf8mb3_general_ci', blank=True, null=True)
    batch_size = models.CharField(max_length=20)
    hsn_code = models.IntegerField(blank=True, null=True)
    ic_code = models.IntegerField(blank=True, null=True)
    inventory_days = models.IntegerField(blank=True, null=True)
    sheme_lot_one_invoice_qnty = models.IntegerField(blank=True, null=True)
    sheme_lot_one_free_qnty = models.IntegerField(blank=True, null=True)
    sheme_lot_two_invoice_qnty = models.IntegerField(blank=True, null=True)
    sheme_lot_two_free_qnty = models.IntegerField(blank=True, null=True)
    min_inventory_qnty = models.IntegerField(blank=True, null=True)
    commission = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'


class Product1(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.TextField()
    sku = models.TextField()
    product_code = models.TextField()
    unit = models.TextField()
    product_division = models.IntegerField()
    sub_division = models.TextField(blank=True, null=True)
    category_id = models.IntegerField()
    manufacturer = models.TextField(blank=True, null=True)
    barcode = models.TextField(blank=True, null=True)
    shipper_size = models.TextField(blank=True, null=True)
    hsn_code = models.TextField(blank=True, null=True)
    ic_code = models.TextField(blank=True, null=True)
    inventory_days = models.TextField(blank=True, null=True)
    sheme_lot_one_invoice_qnty = models.IntegerField()
    sheme_lot_one_free_qnty = models.IntegerField()
    sheme_lot_two_invoice_qnty = models.IntegerField()
    sheme_lot_two_free_qnty = models.IntegerField()
    min_inventory_qnty = models.IntegerField()
    commission = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'product1'


class ProductCatalogue(models.Model):
    product_catalogue_id = models.AutoField(primary_key=True)
    division_id = models.IntegerField()
    file = models.TextField()
    created_on = models.DateTimeField()
    created_by = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'product_catalogue'


class ProductCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'product_category'


class ProductGroup(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'product_group'


class ProductGst(models.Model):
    gst_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    gst = models.FloatField()
    igst = models.FloatField()
    cgst = models.FloatField()
    sgst = models.FloatField()

    class Meta:
        managed = False
        db_table = 'product_gst'


class ProformaInvoice(models.Model):
    pi_no = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    netamount = models.IntegerField()
    discount = models.FloatField()
    gross = models.FloatField()
    created_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'proforma_invoice'


class Reprocess(models.Model):
    reprocess_id = models.AutoField(primary_key=True)
    good_reciept_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    sku = models.CharField(max_length=14, db_collation='utf8mb3_general_ci', blank=True, null=True)
    quantity = models.CharField(max_length=11, db_collation='utf8mb3_general_ci', blank=True, null=True)
    batch_id = models.IntegerField(blank=True, null=True)
    batch = models.CharField(max_length=11, db_collation='utf8mb3_general_ci', blank=True, null=True)
    manfacturing_date = models.CharField(max_length=19, db_collation='utf8mb3_general_ci', blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    mrp = models.CharField(max_length=19, db_collation='utf8mb3_general_ci', blank=True, null=True)
    purchase_rate = models.IntegerField(blank=True, null=True)
    pts = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    ptr = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ptc = models.IntegerField(blank=True, null=True)
    ptv = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    ptk = models.IntegerField(blank=True, null=True)
    margin = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reprocess'


class RequestFinance(models.Model):
    request_id = models.AutoField(primary_key=True)
    vetzone_id = models.IntegerField()
    comment = models.CharField(max_length=100)
    total_due = models.IntegerField()
    status = models.CharField(max_length=1, db_comment='P:pending , A:approve')
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'request_finance'


class Requisition(models.Model):
    requisition_id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField()
    created_by = models.IntegerField()
    status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'requisition'


class RequisitionDetails(models.Model):
    requisition_details_id = models.AutoField(primary_key=True)
    requisition_id = models.IntegerField()
    product_id = models.IntegerField()
    batch_size = models.IntegerField()
    stock_quantity = models.IntegerField()
    required_quantity = models.IntegerField()
    expected_date = models.DateField()
    status = models.CharField(max_length=1)
    three_month_avg = models.IntegerField()
    available_quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'requisition_details'


class ReturnGoods(models.Model):
    return_id = models.AutoField(primary_key=True)
    is_returned = models.CharField(max_length=1, blank=True, null=True)
    created_by = models.IntegerField()
    type = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField()
    returned_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, db_comment='P - Pending\r\nI - Inprocess\r\nC - Completed')

    class Meta:
        managed = False
        db_table = 'return_goods'


class ReturnLrDetails(models.Model):
    lr_detail_id = models.AutoField(primary_key=True)
    lrno = models.TextField()
    return_id = models.IntegerField()
    file = models.TextField()
    is_verified = models.CharField(max_length=1)
    dispatch_date = models.DateTimeField()
    lr_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'return_lr_details'


class Rightoff(models.Model):
    rightoff_id = models.AutoField(primary_key=True)
    good_reciept_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    sku = models.CharField(max_length=14, db_collation='utf8mb3_general_ci', blank=True, null=True)
    quantity = models.CharField(max_length=11, db_collation='utf8mb3_general_ci', blank=True, null=True)
    batch_id = models.IntegerField(blank=True, null=True)
    batch = models.CharField(max_length=11, db_collation='utf8mb3_general_ci', blank=True, null=True)
    manfacturing_date = models.CharField(max_length=19, db_collation='utf8mb3_general_ci', blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    mrp = models.CharField(max_length=19, db_collation='utf8mb3_general_ci', blank=True, null=True)
    purchase_rate = models.IntegerField(blank=True, null=True)
    pts = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    ptr = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ptc = models.IntegerField(blank=True, null=True)
    ptv = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    ptk = models.IntegerField(blank=True, null=True)
    margin = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'rightoff'


class SalesPlan(models.Model):
    sale_plan_id = models.AutoField(primary_key=True)
    plan_amount = models.IntegerField()
    created_by = models.IntegerField()
    created_by_role = models.IntegerField()
    created_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sales_plan'


class SalesPlanMeta(models.Model):
    sales_meta_id = models.AutoField(primary_key=True)
    sales_plan_id = models.IntegerField()
    customer_id = models.IntegerField()
    customer_role = models.TextField()
    plan_value = models.IntegerField()
    status = models.CharField(max_length=1, db_comment='P:Comments\r\nY:Accepted\r\nN:Rejected')

    class Meta:
        managed = False
        db_table = 'sales_plan_meta'


class SalesPlanProductMeta(models.Model):
    sales_plan_product_id = models.AutoField(primary_key=True)
    sales_meta_id = models.IntegerField()
    product_id = models.IntegerField()
    product_quantity = models.IntegerField()
    product_value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sales_plan_product_meta'


class State(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.TextField()
    state_code = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'state'


class Suppliers(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    sup_name = models.TextField()
    sup_email = models.TextField()
    address = models.TextField()
    state_id = models.IntegerField()
    city = models.TextField(blank=True, null=True)
    pincode = models.IntegerField()
    category = models.IntegerField()
    phone = models.TextField(blank=True, null=True)
    gst = models.TextField(blank=True, null=True)
    pan = models.TextField(blank=True, null=True)
    contact_person = models.TextField(blank=True, null=True)
    contact_person_number = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suppliers'


class TargetMeta(models.Model):
    target_meta_id = models.AutoField(primary_key=True)
    target_id = models.IntegerField()
    product_id = models.IntegerField()
    sku = models.TextField()
    pts = models.TextField()
    ypm = models.TextField()
    quantity = models.FloatField()
    value = models.FloatField()
    month = models.TextField()
    year = models.IntegerField()
    created_date = models.DateTimeField()
    status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'target_meta'


class TargetTable(models.Model):
    target_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    hq_id = models.IntegerField()
    desig_id = models.IntegerField()
    file = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField()
    status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'target_table'


class TermsConditions(models.Model):
    terms_id = models.AutoField(primary_key=True)
    cust_type = models.CharField(max_length=11, blank=True, null=True)
    file = models.TextField(blank=True, null=True)
    created_by = models.IntegerField()
    created_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'terms_conditions'


class Vetzone(models.Model):
    vetzone_id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    owner_name = models.TextField()
    email = models.TextField()
    mobile_number = models.TextField()
    password = models.TextField()
    type = models.IntegerField()
    role = models.IntegerField()
    kyc_status = models.CharField(max_length=1)
    approval_status = models.CharField(max_length=1, db_comment='C - Closed VetZone')
    is_registered = models.CharField(max_length=1)
    created_on = models.DateTimeField()
    placeorder = models.CharField(max_length=1)
    state_id = models.IntegerField()
    geo_location = models.CharField(max_length=100, blank=True, null=True)
    establishment_status = models.CharField(max_length=1)
    remark = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vetzone'


class VetzoneBroucher(models.Model):
    vetzone_broucher_id = models.AutoField(primary_key=True)
    division_id = models.IntegerField()
    file = models.TextField(blank=True, null=True)
    created_by = models.IntegerField()
    created_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'vetzone_broucher'


class VetzoneCloseRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    refund_amt = models.TextField()
    document = models.TextField()
    vetzone_id = models.IntegerField()
    created_by = models.IntegerField()
    created_on = models.DateTimeField()
    status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'vetzone_close_request'


class VetzoneCreditNoteTable(models.Model):
    credit_note_id = models.AutoField(primary_key=True)
    amount = models.TextField()
    invoice_date = models.DateTimeField()
    order_id = models.IntegerField()
    user_id = models.IntegerField()
    user_role = models.TextField()
    order_date = models.DateTimeField()
    credit_end_date = models.DateField()
    payment_status = models.CharField(max_length=1, db_comment='Y-Completed\r\nN - Pending\r\nP - pending for approval\r\nD - declined')
    payment_date = models.DateField()
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vetzone_credit_note_table'


class VetzoneEndCustomer(models.Model):
    end_customer_id = models.AutoField(primary_key=True)
    created_by_user_id = models.IntegerField()
    created_by_user_role = models.IntegerField()
    created_date = models.DateTimeField()
    name = models.TextField()
    mobile = models.TextField()
    email = models.TextField()
    farm_name = models.TextField(blank=True, null=True)
    address = models.TextField()
    taluka = models.TextField()
    district = models.TextField(db_column='District')  # Field name made lowercase.
    state = models.TextField(db_column='State')  # Field name made lowercase.
    pin_code = models.TextField(db_column='Pin_code', blank=True, null=True)  # Field name made lowercase.
    gst_no = models.TextField(blank=True, null=True)
    hq = models.IntegerField()
    division = models.IntegerField()
    status = models.CharField(max_length=1)
    farmer_type = models.TextField()
    dairy_animals = models.IntegerField()
    sheep_goat = models.IntegerField()
    piggery_animals = models.IntegerField()
    layer_birds = models.IntegerField()
    broiler_birds = models.IntegerField()
    reference = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vetzone_end_customer'


class VetzoneGoods(models.Model):
    vetzone_goods_id = models.AutoField(primary_key=True)
    vetzone_id = models.IntegerField()
    sim_number = models.IntegerField()
    opening_goods = models.TextField(blank=True, null=True)
    machine = models.TextField(blank=True, null=True)
    furniture = models.TextField(blank=True, null=True)
    machine_file = models.TextField(blank=True, null=True)
    furniture_file = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vetzone_goods'


class VetzoneHqDiv(models.Model):
    vetzone_hq_div_id = models.AutoField(primary_key=True)
    vetzone_id = models.IntegerField()
    hq_id = models.IntegerField()
    div_id = models.IntegerField()
    approval_admin_id = models.IntegerField()
    sub_division = models.TextField()

    class Meta:
        managed = False
        db_table = 'vetzone_hq_div'


class VetzoneInstock(models.Model):
    instock_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    product_id = models.IntegerField()
    sku = models.TextField()
    quantity = models.IntegerField()
    batch = models.TextField()
    manfacturing_date = models.DateField()
    expiry_date = models.DateField()
    mrp = models.FloatField()
    purchase_rate = models.FloatField()
    pts = models.FloatField()
    ptr = models.FloatField()
    ptc = models.FloatField()
    ptv = models.FloatField()
    ptk = models.FloatField()
    margin = models.FloatField()
    created_by = models.IntegerField()
    created_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'vetzone_instock'


class VetzoneKycDocument(models.Model):
    vetzone_kyc_id = models.AutoField(primary_key=True)
    vetzone_id = models.IntegerField()
    document = models.TextField(blank=True, null=True)
    approval_status = models.CharField(max_length=1)
    uploaded_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'vetzone_kyc_document'


class VetzoneMeta(models.Model):
    vetzone_meta_id = models.AutoField(primary_key=True)
    vetzone_id = models.IntegerField()
    vetzone_meta_key = models.TextField()
    vetzone_meta_value = models.TextField()

    class Meta:
        managed = False
        db_table = 'vetzone_meta'


class VetzonePaymentDetails(models.Model):
    payment_id = models.AutoField(primary_key=True)
    vetzone_id = models.IntegerField()
    amount = models.TextField()
    transcation_id = models.TextField()
    reciept = models.TextField()
    payment_date = models.DateTimeField()
    payment_mode = models.TextField()

    class Meta:
        managed = False
        db_table = 'vetzone_payment_details'


class VetzoneType(models.Model):
    v_type_id = models.AutoField(primary_key=True)
    v_type_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'vetzone_type'

class CustomerReferenceName(models.Model):
    reference_id=models.AutoField(primary_key=True)  
    reference_name= models.TextField(blank=True, null=True)  
 
 
    class Meta:
        managed = False
        db_table = 'customer_reference_name' 