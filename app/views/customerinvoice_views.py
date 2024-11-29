from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from app.serializers.customerinvoice_serializers import CustomerinvoiceSerializer
from num2words import num2words
from decimal import Decimal
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from app.permissions import IsCommercialOperationExecutive, IsNonAdminUser

class CustomerinvoiceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsCommercialOperationExecutive,IsNonAdminUser] 
    def get(self, request, order_id):
        with connection.cursor() as cursor:
            # Fetch customer and invoice data
            cursor.execute(""" 
                SELECT 
                    c.name AS name,
                    c.state_id AS state_id, 
                    s.state_code AS state_code, 
                    s.state_name AS state_name,
                    cm_meta.mobile_number AS mobile,
                    CONCAT(cm_meta.addressl1, ' ', cm_meta.addressl2) AS address,
                    cm_meta.taluka AS taluka,
                    cm_meta.district AS district,
                    cm_meta.state AS state,
                    cm_meta.pincode AS pincode,
                    cm_meta.gstin AS gstin,
                    cm_meta.pan AS pan,
                    cm_meta.bank_name AS bank_name,
                    cm_meta.ac_no AS account_no,
                    cm_meta.bank_ifsc AS bank_ifsc,
                    cm_meta.drug_licence_no as drug_licence_no,
                    i.invoice_no AS invoice_no,
                    i.invoice_amount AS invoice_amount,  
                    i.created_date AS invoice_date,
                    o.order_id AS order_id,
                    p.created_date AS placeorder_date
                FROM 
                    customer c
                LEFT JOIN 
                    (SELECT customer_id,
                        MAX(CASE WHEN customer_meta_key = 'mob_no' THEN customer_meta_value END) AS mobile_number,
                        MAX(CASE WHEN customer_meta_key = 'addressl1' THEN customer_meta_value END) AS addressl1,
                        MAX(CASE WHEN customer_meta_key = 'addressl2' THEN customer_meta_value END) AS addressl2,
                        MAX(CASE WHEN customer_meta_key = 'taluka' THEN customer_meta_value END) AS taluka,
                        MAX(CASE WHEN customer_meta_key = 'District' THEN customer_meta_value END) AS district,
                        MAX(CASE WHEN customer_meta_key = 'State' THEN customer_meta_value END) AS state,
                        MAX(CASE WHEN customer_meta_key = 'Pin_code' THEN customer_meta_value END) AS pincode,
                        MAX(CASE WHEN customer_meta_key = 'gst_no' THEN customer_meta_value END) AS gstin,
                        MAX(CASE WHEN customer_meta_key = 'pan_no' THEN customer_meta_value END) AS pan,
                        MAX(CASE WHEN customer_meta_key = 'bank_name' THEN customer_meta_value END) AS bank_name,
                        MAX(CASE WHEN customer_meta_key = 'bank_ac_no' THEN customer_meta_value END) AS ac_no,
                        MAX(CASE WHEN customer_meta_key = 'bank_ifsc' THEN customer_meta_value END) AS bank_ifsc,
                        MAX(CASE WHEN customer_meta_key = 'drug_licence_no' THEN customer_meta_value END) AS drug_licence_no
                    FROM customer_meta
                    GROUP BY customer_id) AS cm_meta ON c.customer_id = cm_meta.customer_id
                LEFT JOIN 
                    order_table_product o ON c.customer_id = o.user_id
                LEFT JOIN 
                    placeorder p ON p.stockiest_order_id = o.order_id
                LEFT JOIN 
                    invoice i ON i.order_id = p.stockiest_order_id
                LEFT JOIN 
                    state s ON c.state_id = s.state_id
                WHERE 
                    o.order_id = %s
            """, [order_id])

            customer_invoice_data = cursor.fetchone()
            if customer_invoice_data:
                columns = [col[0] for col in cursor.description]
                customer_invoice_data = dict(zip(columns, customer_invoice_data))              
                customer_invoice_data['state_id'] = customer_invoice_data.get('state_id') or 0

        # Fetch product details with sr_no indexing
        product_details = []
        total_discounted_amount = Decimal('0')
        bill_total = Decimal('0')
        total_CGST_Amt = Decimal('0')
        total_SGST_Amt = Decimal('0')
        total_IGST_Amt = Decimal('0')
        NET_AMT_cs = Decimal('0')
        NET_AMT_i= Decimal('0')
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    p.hsn_code AS hsn_code,
                    p.product_name AS product_name,
                    p.sku AS sku,
                    otp.batch AS batch,
                    i.expiry_date AS expiry_date,
                    otp.quantity AS quantity,
                    otp.free AS free,
                    i.mrp AS mrp,
                    i.pts AS pts,
                    i.ptr AS ptr,
                    otp.rate AS rate,  -- Ensure rate is fetched
                    (otp.quantity * i.pts) AS amount,
                    otp.disc AS disc,
                    pg.gst AS gst_rate,
                    pg.igst AS igst_rate,
                    pg.cgst AS cgst_rate,
                    pg.sgst AS sgst_rate,
                    inv.invoice_amount AS invoice_amount 
                FROM 
                    order_table_product otp
                JOIN 
                    instock i 
                    ON otp.product_id = i.product_id AND otp.batch = i.batch
                JOIN 
                    product p 
                    ON otp.product_id = p.product_id
                LEFT JOIN 
                    product_gst pg 
                    ON p.product_id = pg.product_id
                LEFT JOIN 
                    invoice inv ON otp.order_id = inv.order_id
                WHERE 
                    otp.order_id = %s;
            """, [order_id])

            product_columns = [col[0] for col in cursor.description]
            product_details = [
                dict(zip(product_columns, row))
                for row in cursor.fetchall()
            ]
            for index, product in enumerate(product_details):
                product['sr_no'] = index + 1

                # Convert amount to Decimal if it's not already
                amount = Decimal(product.get('amount', 0))
                product['amount'] = amount

                discounted_amount = amount * Decimal(product['disc']) / Decimal('100')
                product['discounted_amount'] = discounted_amount

                total_discounted_amount += discounted_amount
                # Calculate taxable amount (using Decimal for precision)
                product['taxable'] = amount - (amount * Decimal(product['disc']) / Decimal('100'))

                # Fetch GST rates
                product['IGST_per'] = Decimal(product.get('igst_rate', 0))
                product['CGST_per'] = Decimal(product.get('cgst_rate', 0))
                product['SGST_per'] = Decimal(product.get('sgst_rate', 0))

                # Calculate GST amounts using Decimal for precision
                product['IGST_Amt'] = (product['taxable'] * product['IGST_per']) / Decimal('100')
                product['CGST_Amt'] = (product['taxable'] * product['CGST_per']) / Decimal('100')
                product['SGST_Amt'] = (product['taxable'] * product['SGST_per']) / Decimal('100')

                total_IGST_Amt += product['IGST_Amt']
                total_CGST_Amt += product['CGST_Amt']
                total_SGST_Amt += product['SGST_Amt']
                total_gst_cs = total_CGST_Amt + total_SGST_Amt
                bill_total += amount

                # NET_AMT_cs= bill_total-total_discounted_amount+total_gst_cs
                # NET_AMT_cs = round(NET_AMT_cs, 2)
                NET_AMT_cs = (bill_total - total_discounted_amount + total_gst_cs).quantize(Decimal('0.01'))
                customer_invoice_data['NET_AMT_cs'] = NET_AMT_cs
                NET_AMT_i= bill_total-total_discounted_amount+total_IGST_Amt
                NET_AMT_i = round(NET_AMT_i, 2)
            
                
                customer_invoice_data['less'] = total_discounted_amount
                customer_invoice_data['bill_total'] = bill_total
                customer_invoice_data['total_CGST_Amt'] = total_CGST_Amt
                customer_invoice_data['total_SGST_Amt'] = total_SGST_Amt
                customer_invoice_data['total_gst_cs'] = total_gst_cs
                customer_invoice_data['total_gst_I'] = total_IGST_Amt
                # customer_invoice_data['NET_AMT_cs'] = total_gst_cs
                customer_invoice_data['NET_AMT_i'] = NET_AMT_i

            if customer_invoice_data and 'invoice_amount' in customer_invoice_data and customer_invoice_data['invoice_amount']:
        # Convert invoice amount to words using Indian numbering system
                customer_invoice_data['invoice_amount_words'] = num2words(
                    customer_invoice_data['invoice_amount'],
                    lang='en_IN'
                ).capitalize() + " rupees only"
            else:
                customer_invoice_data['invoice_amount_words'] = "N/A"

            if customer_invoice_data['state_code'] == 27:
                net_amt = NET_AMT_cs
                net_amt_words = customer_invoice_data['invoice_amount_words']
            else:
                net_amt = NET_AMT_i
                net_amt_words = customer_invoice_data['invoice_amount_words']

        # Pass data to the serializer
        serializer = CustomerinvoiceSerializer({
            **customer_invoice_data,
            "net_amt": net_amt,
            "net_amt_words": net_amt_words,
            "products": product_details
        })
        return Response(serializer.data)

# http://54.245.186.61:8000/app/Customer_invoice/6406/