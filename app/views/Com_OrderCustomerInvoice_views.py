from decimal import Decimal
from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView
from app.serializers.Com_OrderCustomerInvoice_serializers import ComBatchAllocatedInvoiceSerializer
from rest_framework import status
from collections import namedtuple
from num2words import num2words
from datetime import datetime
from django.db import transaction
from django.utils.timezone import now  # Use timezone-aware dates
from decimal import Decimal, InvalidOperation
from rest_framework import status
from rest_framework.response import Response
from django.db import connection, transaction
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from app.permissions import IsCommercialOperationManager,IsNonAdminUser

class ComBatchAllocatedInvoiceView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsCommercialOperationManager,IsNonAdminUser] 

    def get(self, request, order_id=None):
        # Extract discount values for each product from the request (default to 0 if not provided)
        discounts = request.query_params.getlist('disc', [])  # E.g., disc=10&disc=5 for multiple products

        with connection.cursor() as cursor:
            # Fetch customer and invoice data
            cursor.execute(""" 
                SELECT 
                    c.name AS name,
                    c.state_id AS state_id, 
                    s.state_name AS state_name,
                    s.state_code AS state_code, 
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

            # Fetch product details
            cursor.execute("""
                SELECT 
                    p.hsn_code AS hsn_code,
                    p.product_name AS product_name,
                    p.sku AS sku,
                    otp.batch AS batch,
                    i.expiry_date AS expiry_date,
                    otp.quantity AS quantity,
                    otp.free AS free,
                    otp.product_id,
                    i.mrp AS mrp,
                    i.pts AS pts,
                    i.ptr AS ptr,
                    otp.rate AS rate,  
                    (otp.quantity * i.pts) AS amount,
                    pg.gst AS gst_rate,
                    pg.igst AS igst_rate,
                    pg.cgst AS cgst_rate,
                    pg.sgst AS sgst_rate
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
                WHERE 
                    otp.order_id = %s;
            """, [order_id])

            product_columns = [col[0] for col in cursor.description]
            product_details = [
                dict(zip(product_columns, row))
                for row in cursor.fetchall()
            ]

            # Perform calculations dynamically for each product
            total_discounted_amount = Decimal(0)
            total_IGST_Amt = Decimal(0)
            total_CGST_Amt = Decimal(0)
            total_SGST_Amt = Decimal(0)
            bill_total = Decimal(0)

            for index, product in enumerate(product_details):
                product['sr_no'] = index + 1

                # Fetch the discount for the current product
                product_discount = Decimal(discounts[index]) if index < len(discounts) else Decimal(0)

                # Calculate amount and discount
                amount = Decimal(product.get('amount', 0))
                product['amount'] = amount

                discounted_amount = (amount * product_discount) / Decimal('100')
                product['discounted_amount'] = discounted_amount

                total_discounted_amount += discounted_amount

                # Calculate taxable amount
                taxable = amount - discounted_amount
                product['taxable'] = taxable

                # Calculate GST
                
                product['CGST_Amt'] = (taxable * Decimal(product['cgst_rate'])) / Decimal('100')
                product['SGST_Amt'] = (taxable * Decimal(product['sgst_rate'])) / Decimal('100')
                product['IGST_Amt'] = (taxable * Decimal(product['igst_rate'])) / Decimal('100') # No IGST for Maharashtra
                total_CGST_Amt += product['CGST_Amt']
                total_SGST_Amt += product['SGST_Amt']
                total_IGST_Amt += product['IGST_Amt']

                # Accumulate the bill total
                bill_total += amount


            # Final totals
            total_gst_cs = total_CGST_Amt + total_SGST_Amt
            NET_AMT_cs = (bill_total - total_discounted_amount + total_gst_cs).quantize(Decimal('0'))
            NET_AMT_i = (bill_total - total_discounted_amount + total_IGST_Amt).quantize(Decimal('0'))
            # NET_AMT_i = float(bill_total) - float(total_discounted_amount) + float(total_CGST_Amt) + float(total_SGST_Amt)
            # Convert NET_AMT_cs and NET_AMT_i to words
            customer_invoice_data['NET_AMT_cs_words'] = (
                num2words(NET_AMT_cs, lang='en_IN').capitalize() + " rupees only"
                if NET_AMT_cs > 0 else "N/A"
            )

            customer_invoice_data['NET_AMT_i_words'] = (
                num2words(NET_AMT_i, lang='en_IN').capitalize() + " rupees only"
                if NET_AMT_i > 0 else "N/A"
            )
            if customer_invoice_data['state_code'] == 27:
                net_amt = NET_AMT_cs
                net_amt_words = customer_invoice_data['NET_AMT_cs_words']
            else:
                net_amt = NET_AMT_i
                net_amt_words = customer_invoice_data['NET_AMT_i_words']


        customer_invoice_data.update({
            'less': total_discounted_amount,
            'bill_total': bill_total,
            'total_CGST_Amt': total_CGST_Amt,
            'total_SGST_Amt': total_SGST_Amt,
            'total_gst_cs': total_CGST_Amt + total_SGST_Amt,
            'total_gst_I': total_IGST_Amt,  # Add IGST total here
            'NET_AMT_cs': NET_AMT_cs,
            'NET_AMT_i': NET_AMT_i,
            'NET_AMT_cs_words': customer_invoice_data['NET_AMT_cs_words'],
            'NET_AMT_i_words': customer_invoice_data['NET_AMT_i_words'],
            'net_amt': net_amt,  # Include net_amt
            'net_amt_words': net_amt_words,  # Include net_amt_words
        })


        serializer = ComBatchAllocatedInvoiceSerializer({
            **customer_invoice_data,  # Contains all the customer/invoice data
            "products": product_details,  # Contains the list of products
        })

        # Return the serialized response
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, order_id=None):
        try:
            # Extract discounts, taxable amounts, and invoice data
            products = request.data.get("products", [])
            if not products or not isinstance(products, list):
                return Response({"error": "Products must be provided as a list."}, status=status.HTTP_400_BAD_REQUEST)

            current_year = datetime.now().year
            current_month = datetime.now().month

            # Determine the financial year
            if current_month > 3:
                financial_year = f"{current_year}-{current_year + 1 % 100:02d}"
            else:
                financial_year = f"{current_year - 1}-{current_year % 100:02d}"

            # Fetch the latest invoice number and determine the next one
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT invoice_no 
                    FROM invoice 
                    WHERE invoice_no LIKE %s
                    ORDER BY invoice_id DESC
                    LIMIT 1
                """, [f"VH{financial_year}/%"])
                last_invoice = cursor.fetchone()

                if last_invoice and last_invoice[0]:
                    last_number = int(last_invoice[0].split('/')[-1])  # Extract the last number
                    next_invoice_no = f"VH{financial_year}/{last_number + 1}"
                else:
                    next_invoice_no = f"VH{financial_year}/1"  # Start with 1 if no invoice exists
            
            net_amt = Decimal(request.data.get('net_amt', 0)) 

            # Calculate invoice totals
            with transaction.atomic():
                # Ensure the cursor remains within the transaction.atomic() block
                with connection.cursor() as cursor:
                    for product in products:
                        disc = Decimal(product.get("disc", 0))
                        taxable = Decimal(product.get("taxable", 0))

                        # Insert product-specific data into `order_table_product`
                        cursor.execute(
                            "UPDATE order_table_product SET disc = %s, tax = %s WHERE order_id = %s",
                            [disc, taxable, order_id],
                        )

                    # Insert invoice data
                    current_date = datetime.now()
                    cursor.execute("""
                        INSERT INTO invoice (invoice_no, order_id, invoice_amount, created_date)
                        VALUES (%s, %s, %s, %s)
                    """, [next_invoice_no, order_id,net_amt, current_date])

            return Response({
                "message": "Invoice created successfully.",
                "invoice_no": next_invoice_no,
                "invoice_amount": net_amt,
                "order_id": order_id,
                "created_date": current_date
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
