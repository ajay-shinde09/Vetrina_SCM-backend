from django.http import JsonResponse
from django.views import View
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from decimal import Decimal
from num2words import num2words

class GenerateInvoiceAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_user_from_token(self, request):
        """
        Extract user_id and role_name from the access token in the Authorization header.
        """
        auth = JWTAuthentication()
        try:
            token = request.headers.get('Authorization', '').split(' ')[1]
            validated_token = auth.get_validated_token(token)
            user_id = validated_token.get('customer_id')
            role_name = validated_token.get('role_name')
            if not user_id or not role_name:
                return None, None
            return user_id, role_name
        except (InvalidToken, TokenError, IndexError):
            return None, None

    def get(self, request, *args, **kwargs):
        try:
            user_id, role_name = self.get_user_from_token(request)
            if not user_id or not role_name:
                return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

            order_id = request.GET.get('order_id')
            if not order_id:
                return JsonResponse({'error': 'order_id is required.'}, status=400)

            with connection.cursor() as cursor:
                # Query for customer and invoice details
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
                        cm_meta.drug_licence_no AS drug_licence_no,
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
                if not customer_invoice_data:
                    return JsonResponse({'error': 'Invoice details not found.'}, status=404)

                columns = [col[0] for col in cursor.description]
                customer_invoice_data = dict(zip(columns, customer_invoice_data))

            # Query for product details
            product_details = []
            total_discounted_amount = Decimal('0')
            total_gst_cs = Decimal('0')
            total_gst_i = Decimal('0')
            bill_total = Decimal('0')
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
                        otp.rate AS rate,
                        (otp.quantity * i.pts) AS amount,
                        otp.disc AS disc,
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
                product_details = [dict(zip(product_columns, row)) for row in cursor.fetchall()]
                for product in product_details:
                    amount = Decimal(product.get('amount', 0))
                    discount = Decimal(product.get('disc', 0))
                    taxable = amount - (amount * discount / Decimal(100))
                    product['taxable'] = taxable
                    product['CGST_Amt'] = (taxable * Decimal(product['cgst_rate'])) / Decimal(100)
                    product['SGST_Amt'] = (taxable * Decimal(product['sgst_rate'])) / Decimal(100)
                    product['IGST_Amt'] = (taxable * Decimal(product['igst_rate'])) / Decimal(100)

            # Invoice amount in words
            customer_invoice_data['invoice_amount_words'] = num2words(
                customer_invoice_data['invoice_amount'], lang='en_IN'
            ).capitalize() + " rupees only"

            return JsonResponse({
                'invoice': customer_invoice_data,
                'products': product_details,
            }, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)